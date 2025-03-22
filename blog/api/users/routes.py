import logging
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt
from blog.models import User
from blog.extension import db

class User(Resource):
    @jwt_required()
    def get(self):
        """获取用户列表，仅限管理员操作"""
        code = None
        message = None
        data = None
        try:
            # 获取用户名
            username = get_jwt()['username']
            if username == 'Admin':
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
        except Exception as e:
            logging.error(e)
            code = 500
            message = str(e)
            return jsonify({'code': code, 'message': message})

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
            code = 200
            message = 'Success create user'
            return jsonify({'code': code, 'message': message})
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            code = 500
            message = str(e)
            return jsonify({'code': code, 'message': message})