import datetime

from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt
from blog.extension import redis_client
from blog.models import User
from blog.extension import db


class AuthLogin(Resource):
    def post(self):
        code = None
        message = None
        token = None
        userid = None
        # 解析参数
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, location='json', help='用户名不能为空')
        parser.add_argument('password', type=str, required=True, location='json', help='密码不能为空')
        args = parser.parse_args()

        username = args['username']
        password = args['password']
        # print("username:", username, "password:", password)

        # 验证用户名密码
        try:
            flag_user_exist, flag_password_correct, user = User.authenticate(username, password)
            if not flag_user_exist:
                code = 404
                message = '用户不存在'
            elif not flag_password_correct:
                code = 400
                message = '密码错误'
            else:
                code = 200
                message = '登录成功'
                # 将用户状态设置为1
                user.status = 1
                db.session.commit()
                # 创建jwt token，设置好过期时间
                token = create_access_token(identity={
                    'user_id': user.user_id,
                    'username': user.username
                }, expires_delta=datetime.timedelta(seconds=3600))
                userid = user.user_id

            return jsonify({'code': code, 'message': message, 'token': token, 'userid': userid})
        except Exception as e:
            code = 400
            message = '登录失败'
            return jsonify({'code': code, 'message': message, 'error': str(e)})


class AuthLogout(Resource):
    @jwt_required
    def get(self):
        code = None
        message = None
        try:
            # 获取当前用户的 token
            jti_info = get_jwt()
            jti = jti_info['jti']
            user_id = jti_info['user_id']
            # 将token 添加到黑名单中
            redis_client.set(jti, 'true', 3600)
            # 设置用户状态
            user = User.query.get(user_id)
            user.status = 0
            db.session.commit()

            # 设置状态码等信息
            code = 200
            message = "登出成功"
            return jsonify({'code': code, 'message': message})
        except Exception as e:
            code = 400
            message = "登出失败"
            return jsonify({'code': code, 'message': message, 'error': str(e)})
