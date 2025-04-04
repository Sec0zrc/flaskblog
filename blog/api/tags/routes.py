import logging
from flask import jsonify
from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError

from blog.extension import db
from blog.api.users.routes import is_admin
from blog.models import Tag, Post
from flask_jwt_extended import jwt_required


class Tags(Resource):

    def get(self, tag_id=None):
        code = None
        message = None

        # 如果tag_id不为空，返回所有该tag的文章列表
        if tag_id:
            try:
                posts = db.session.query(Tag).join(Tag.posts).filter(Tag.tag_id == tag_id).all()
                posts_list = []
                if posts:
                    for post in posts:
                        posts_list.append({
                            'post_id': post.post_id,
                            'title': post.title,
                            'content': post.content,
                            'create_at': post.create_at,
                            'status': post.status,
                            'category_id': post.category_id,
                        })
                    code = 200
                    message = 'success'
                    return jsonify({'code': code, 'message': message, 'data': posts_list})
                else:
                    code = 404
                    message = 'posts not found'
                    return jsonify({'code': code, 'message': message})
            except SQLAlchemyError as e:
                db.session.rollback()
                code = 400
                message = 'bad request'
                logging.error(e)
                return jsonify({'code': code, 'message': message, "error": str(e)})
            except Exception as e:
                db.session.rollback()
                code = 400
                message = 'bad request'
                logging.error(e)
                return jsonify({'code': code, 'message': message, "error": str(e)})

        # 如果tag_id 为None
        try:
            tags = Tag.query.all()
            tags_list = []
            if tags:
                for tag in tags:
                    tags_list.append({
                        'tag_id': tag.tag_id,
                        'tag_name': tag.tag_name
                    })
                code = 200
                message = 'success'
                return jsonify({'code': code, 'message': message, 'data': tags_list})
            else:
                code = 404
                message = 'tags not found'
                return jsonify({'code': code, 'message': message})
        except Exception as e:
            code = 500
            message = 'internal server error'
            logging.error(e)
            return jsonify({'code': code, 'message': message})

    @jwt_required()
    def post(self):
        code = None
        message = None

        # check admin
        if is_admin():
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('tag_name', type=str, required=True, help='tag_name is required')
                args = parser.parse_args()

                tag_name = args['tag_name']
                if Tag.query.filter_by(tag_name=tag_name).first():
                    code = 400
                    message = 'tag already exists'
                    return jsonify({'code': code, 'message': message})
                else:
                    tag = Tag(tag_name)
                    db.session.add(tag)
                    db.session.commit()
                    code = 201
                    message = 'tag created'
                    return jsonify({'code': code, 'message': message})
            except SQLAlchemyError as e:
                db.session.rollback()
                code = 400
                message = 'bad request'
                logging.error(e)
                return jsonify({'code': code, 'message': message, "error": str(e)})
            except Exception as e:
                code = 500
                message = 'internal server error'
                logging.error(e)
                return jsonify({'code': code, 'message': message, "error": str(e)})
        else:
            code = 401
            message = 'unauthorized'
            return jsonify({'code': code, 'message': message})

    @jwt_required()
    def delete(self, tag_id):
        code = None
        message = None
        if is_admin():
            try:
                tag = Tag.query.filter_by(tag_id=tag_id).first()
                if tag:
                    # delete the foreign key in post table
                    post = Post.query.filter_by(tag_id=tag_id)
                    for p in post:
                        p.tag_id = None
                        db.session.commit()

                    db.session.delete(tag)
                    db.session.commit()
                    code = 200
                    message = 'tag deleted'
                    return jsonify({'code': code, 'message': message})
                else:
                    code = 404
                    message = 'tag not found'
                    return jsonify({'code': code, 'message': message})
            except SQLAlchemyError as e:
                db.session.rollback()
                code = 400
                message = 'bad request'
                logging.error(e)
                return jsonify({'code': code, 'message': message, "error": str(e)})
            except Exception as e:
                code = 500
                message = 'internal server error'
                logging.error(e)
                return jsonify({'code': code, 'message': message, "error": str(e)})
        else:
            code = 401
            message = 'unauthorized'
            return jsonify({'code': code, 'message': message})