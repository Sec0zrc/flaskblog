import logging
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from blog.models import User
from blog.extension import db


def is_admin():
    if get_jwt()['jti']['username'] == 'Admin':
        return True
    else:
        return False


class Users(Resource):
    @jwt_required()
    def get(self):
        """获取用户列表，仅限管理员操作"""
        code = None
        message = None
        data = None
        try:

            if is_admin():
                users = User.query.all()
                user_list = []
                for user in users:
                    user_dict = {
                        'user_id': user.user_id,
                        'username': user.username,
                        'create_at': user.create_at
                    }
                    user_list.append(user_dict)
                code = 200
                message = 'success'
                data = user_list
                return jsonify({'code': code, 'message': message, 'data': user_list})
            else:
                code = 403
                message = 'Permission denied'
                return jsonify({'code': code, 'message': message}), 403
        except SQLAlchemyError as e:
            # 针对数据库异常进行回滚操作
            code = 500
            message = '用户列表获取失败'
            db.session.rollback()
            logging.error(e)
            return jsonify({'code': code, 'message': message, 'error': str(e)})
        except Exception as e:
            logging.error(e)
            code = 500
            message = "用户列表获取失败"
            return jsonify({'code': code, 'message': message, 'error': str(e)})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='username is required')
        parser.add_argument('password', type=str, required=True, help='password is required')
        args = parser.parse_args()

        code = None
        message = None

        try:
            username = args['username']
            password = args['password']
            user = User(username, password)
            db.session.add(user)
            db.commit()
            code = 201
            message = 'success'
            return jsonify({'code': code, 'message': message})
        except SQLAlchemyError as e:
            # 针对数据库异常进行回滚操作
            code = 500
            message = '用户创建失败'
            db.session.rollback()
            logging.error(e)
            return jsonify({'code': code, 'message': message, 'error': str(e)})
        except Exception as e:
            code = 500
            error = str(e)
            message = "用户创建失败"
            logging.error(e)
            return jsonify({'code': code, 'message': message, 'error': error})

    @jwt_required()
    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str, required=True, help='password')
        password = parser.parse_args()

        code = None
        message = None

        try:
            if not is_admin():
                code = 403
                message = "Permission denial!"
                return jsonify({'code': code, 'message': message})
            else:
                user = User.query.get(user_id)
                if user:
                    user.set_password(password)
                    db.session.commit()
                    code = 200
                    message = "用户密码修改成功"
                else:
                    code = 404
                    message = "用户不存在"
                return jsonify({'code': code, 'message': message})
        except SQLAlchemyError as e:
            # 针对数据库异常进行回滚操作
            code = 500
            message = '用户密码修改失败'
            db.session.rollback()
            logging.error(e)
            return jsonify({'code': code, 'message': message, 'error': str(e)})
        except Exception as e:
            code = 500
            message = "用户密码修改失败"
            error = str(e)
            return jsonify({'code': code, 'message': message, 'error': error})

    @jwt_required
    def delete(self, user_id):
        code = None
        message = None

        try:
            if is_admin():
                user = User.query.get(user_id)
                if user:
                    db.session.delete(user)
                    db.session.commit()
                    code = 200
                    message = "用户删除成功"
                else:
                    code = 404
                    message = "用户不存在"
                return jsonify({'code': code, 'message': message})
            else:
                code = 403
                message = "Permission denial!"
                return jsonify({'code': code, 'message': message})
        except SQLAlchemyError as e:
            # 针对数据库异常进行回滚操作
            code = 500
            message = '用户删除失败'
            db.session.rollback()
            logging.error(e)
            return jsonify({'code': code, 'message': message, 'error': str(e)})
        except Exception as e:
            db.session.rollback()
            code = 500
            message = "用户删除失败"
            error = str(e)
            return jsonify({'code': code, 'message': message, 'error': error})
