import logging
from sqlalchemy.exc import SQLAlchemyError
from blog.api.users.routes import is_admin
from blog.models import Post, Category, Tag
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource, reqparse
from datetime import datetime
from blog.extension import db


class Posts(Resource):

    # 获取文章列表,根据分页来获取
    def get(self, post_id=None):
        # 解析参数
        code = None
        message = None
        data = None

        if post_id is not None:
            # 返回指定文章内容
            try:
                post = Post.query.get(post_id)
                if post:
                    code = 200
                    message = '获取文章成功'
                    data = {
                        'post_id': post.post_id,
                        'title': post.title,
                        'content': post.content,
                        'create_at': post.create_at,
                        'status': post.status,
                        'category_id': post.category_id,
                        'tag_id': post.tag_id,
                        'user_id': post.user_id
                    }
                    return jsonify({'code': code, 'message': message, 'data': data})
                else:
                    code = 404
                    message = '文章不存在'
                    return jsonify({'code': code, 'message': message})
            except SQLAlchemyError as e:
                # 针对数据库异常进行回滚操作
                code = 500
                message = '获取文章失败'
                db.session.rollback()
                logging.error(e)
                return jsonify({'code': code, 'message': message, 'error': str(e)})
            except Exception as e:
                code = 500
                message = '获取文章失败'
                logging.error(e)
                return jsonify({'code': code, 'message': message, 'data': data, 'error': str(e)})
        else:
            # 获取文章列表信息
            try:
                page_num = request.args.get('page', 1, type=int)
                per_page_num = request.args.get('per_page', 10, type=int)
                logging.info(f'page: {page_num}, per_page: {per_page_num}')

                if page_num < 1:
                    code = 400
                    message = '获取文章列表失败'
                    logging.info(f'page: {page_num}, per_page: {per_page_num}')
                    return jsonify({'code': code, 'message': message})

                if per_page_num < 1:
                    code = 400
                    message = '获取文章列表失败'
                    logging.info(f'page: {page_num}, per_page: {per_page_num}')
                    return jsonify({'code': code, 'message': message})

                posts = Post.query.paginate(page=page_num, per_page=per_page_num, error_out=None)
                posts_info = []

                if posts:
                    if page_num > posts.pages:
                        code = 400
                        message = '获取文章列表失败，超出范围'
                        return jsonify({'code': code, 'message': message})

                    for post in posts:
                        posts_info.append({
                            'post_id': post.post_id,
                            'title': post.title,
                            'create_at': post.create_at,
                            'status': post.status,
                            'category_id': post.category_id,
                            'tag_id': post.tag_id,
                        })
                    data = {
                        'posts': posts_info,
                        'total': posts.total,
                        'page': posts.page,
                        'pages': posts.pages,
                        'per_page': posts.per_page
                    }
                    code = 200
                    message = '获取文章列表成功'
                    return jsonify({'code': code, 'message': message, 'data': data})
                else:
                    code = 400
                    message = '文章列表为空'
                    return jsonify({'code': code, 'message': message})
            except SQLAlchemyError as e:
                # 针对数据库异常进行回滚操作
                code = 500
                message = '获取文章列表失败'
                db.session.rollback()
                logging.error(e)
                return jsonify({'code': code, 'message': message, 'error': str(e)})
            except Exception as e:
                code = 500
                message = '获取文章列表失败'
                logging.error(e)
                return jsonify({'code': code, 'message': message, 'data': data, 'error': str(e)})

    @jwt_required
    def post(self):
        # 获取当前用户id
        jti_info = get_jwt()
        jti = jti_info['jti']
        user_id = jti_info['user_id']
        # 检查用户是否为Admin
        if jti['username'] != 'Admin':
            code = 403
            message = 'Permission denial.'
            return jsonify({'code': code, 'message': message})

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='标题不能为空')
        parser.add_argument('content', type=str, required=True, help='内容不能为空')
        parser.add_argument('category', type=str, required=True, help='分类不能为空')
        parser.add_argument('tag', type=str, required=True, help='标签不能为空')
        parser.add_argument('status', type=str, required=True, help='文章状态不能为空')
        args = parser.parse_args()

        try:
            # 获取category和tag的id
            category_id = 0
            tag_id = 0
            if Category.get_id(args['category']):
                category_id = Category.get_id(args['category'])
            else:
                category = Category(args['category'])
                db.session.add(category)
                db.session.commit()
                category_id = Category.get_id(args['category'])

            if Tag.get_id(args['tag']):
                tag_id = Tag.get_id(args['tag'])
            else:
                tag = Tag(args['tag'])
                db.session.add(tag)
                db.session.commit()
                tag_id = Tag.get_id(args['tag'])

            post = Post(args['title'], args['content'], user_id, category_id, tag_id)
            post.set_create_time(datetime.now())
            post.set_status(args['status'])
            db.session.add(post)
            db.session.commit()
            code = 200
            message = '添加文章成功'
            return jsonify({'code': code, 'message': message})
        except SQLAlchemyError as e:
            # 针对数据库异常进行回滚操作
            code = 500
            message = '添加文章失败'
            db.session.rollback()
            logging.error(e)
            return jsonify({'code': code, 'message': message, 'error': str(e)})
        except Exception as e:
            code = 500
            message = '添加文章失败'
            logging.error(e)
            return jsonify({'code': code, 'message': message, 'error': str(e)})

    @jwt_required
    def put(self, post_id):
        """全量更新文章"""
        code = None
        message = None

        # 验证管理员权限
        jti_info = get_jwt()
        jti = jti_info['jti']
        user_id = jti_info['user_id']
        if jti['username'] != 'Admin':
            code = 403
            message = 'Permission denial.'
            return jsonify({'code': code, 'message': message})
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('title', type=str, required=True, help='标题不能为空')
            parser.add_argument('content', type=str, required=True, help='内容不能为空')
            parser.add_argument('category', type=str, required=True, help='分类不能为空')
            parser.add_argument('tag', type=str, required=True)
            parser.add_argument('status', type=str, required=True, help='文章状态不能为空')
            args = parser.parse_args()
            try:
                post = Post.query.get(post_id)
                if post:
                    # 获取category和tag的id
                    category_id = 0
                    tag_id = 0
                    if Category.get_id(args['category']):
                        category_id = Category.get_id(args['category'])
                    else:
                        category = Category(args['category'])
                        db.session.add(category)
                        db.session.commit()
                        category_id = Category.get_id(args['category'])

                    if Tag.get_id(args['tag']):
                        tag_id = Tag.get_id(args['tag'])
                    else:
                        tag = Tag(args['tag'])
                        db.session.add(tag)
                        db.session.commit()
                        tag_id = Tag.get_id(args['tag'])

                    post.set_title(args['title'])
                    post.set_content(args['content'])
                    post.set_category_id(category_id)
                    post.set_tag_id(tag_id)
                    post.set_status(args['status'])
                    db.session.commit()
                    code = 200
                    message = '更新文章成功'
                    return jsonify({'code': code, 'message': message})
                else:
                    code = 404
                    message = '文章不存在'
                    return jsonify({'code': code, 'message': message})
            except SQLAlchemyError as e:
                # 针对数据库异常进行回滚操作
                code = 500
                message = '更新文章失败'
                db.session.rollback()
                logging.error(e)
                return jsonify({'code': code, 'message': message, 'error': str(e)})
            except Exception as e:
                # 其他异常处理
                code = 500
                message = '更新文章失败'
                logging.error(e)
                return jsonify({'code': code, 'message': message, 'error': str(e)})

    @jwt_required
    def put(self, post_id):
        """跟新文章状态"""
        code = None
        message = None

        if is_admin():
            parser = reqparse.RequestParser()
            parser.add_argument('status', type=int, required=True, help='文章状态不能为空')
            args = parser.parse_args()

            try:
                post = Post.query.get(post_id)
                if post:
                    post.set_status(args['status'])
                    db.session.commit()
                    code = 200
                    message = '更新文章状态成功'
                    return jsonify({'code': code, 'message': message})
                else:
                    code = 404
                    message = '文章不存在'
                    return jsonify({'code': code, 'message': message})
            except SQLAlchemyError as e:
                # 针对数据库异常进行回滚操作
                code = 500
                message = '更新文章状态失败'
                db.session.rollback()
                logging.error(e)
                return jsonify({'code': code, 'message': message, 'error': str(e)})
            except Exception as e:
                # 其他异常处理
                code = 500
                message = '更新文章状态失败'
                logging.error(e)
                return jsonify({'code': code, 'message': message, 'error': str(e)})
        else:
            code = 403
            message = 'Permission denial.'
            return jsonify({'code': code, 'message': message})

    @jwt_required
    def delete(self, post_id):
        code = None
        message = None

        if is_admin():
            try:
                post = Post.query.get(post_id)
                if post:
                    db.session.delete(post)
                    db.session.commit()
                    code = 200
                    message = '删除文章成功'
                    return jsonify({'code': code, 'message': message})
                else:
                    code = 404
                    message = '文章不存在'
                    return jsonify({'code': code, 'message': message})
            except SQLAlchemyError as e:
                code = 500
                message = '删除文章失败'
                db.session.rollback()
                logging.error(e)
                return jsonify({'code': code, 'message': message, 'error': str(e)})
            except Exception as e:
                code = 500
                message = '删除文章失败'
                logging.error(e)
                return jsonify({'code': code, 'message': message, 'error': str(e)})
        else:
            code = 403
            message = 'Permission denial.'
            return jsonify({'code': code, 'message': message})
