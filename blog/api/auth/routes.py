import datetime
import logging
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token, get_jwt, set_access_cookies
from sqlalchemy.exc import SQLAlchemyError

from blog.extension import redis_client
from blog.models import User
from blog.extension import db

logging.basicConfig(level=logging.INFO)


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
        result = User.authenticate(username, password)
        flag_user_exist = result[0]
        flag_password_correct = result[1]
        user = result[2]
        logging.info(f'flag_user_exist:{flag_user_exist}, flag_password_correct:{flag_password_correct}, user:{user}')

        try:
            if not flag_user_exist:
                code = 404
                message = '用户不存在'
                return jsonify({'code': code, 'message': message})
            if not flag_password_correct:
                code = 400
                message = '密码错误'
                return jsonify({'code': code, 'message': message})
            elif user.check_status():
                code = 200
                message = '登录成功'
                # 将用户状态设置为1
                user = User.query.get(user.user_id)
                user.status = 1
                db.session.commit()
                # 创建jwt token，设置好过期时间

                token = create_access_token(identity=str(user.user_id),
                                            additional_claims={'username': user.username},
                                            expires_delta=datetime.timedelta(seconds=3600))
                userid = user.user_id
                response = jsonify({'code': code, 'message': message, 'token': token, 'userid': userid})
                # response.set_cookie('token', token, expires=3600, secure=True, httponly=True)
                set_access_cookies(response, token)
                return response
            else:
                # user status为1，表示已登录
                code = 400
                message = '用户已被锁定'
                userid = user.user_id
                return jsonify({'code': code, 'message': message})
        except SQLAlchemyError as e:
            # 针对数据库异常进行回滚操作
            code = 500
            message = '登录失败'
            db.session.rollback()
            logging.error(e)
            return jsonify({'code': code, 'message': message, 'error': str(e)})
        except Exception as e:
            code = 500
            message = '登录失败'
            # logging.info(str(e))
            logging.error(f"Exception occurred: {e}")
            return jsonify({'code': code, 'message': message, 'error': str(e)})


class AuthLogout(Resource):
    @jwt_required()
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
            if user is None:
                code = 404
                message = "用户不存在"
                return jsonify({'code': code, 'message': message})
            user.status = 0
            db.session.commit()

            # 设置状态码等信息
            code = 200
            message = "登出成功"
            # 删除用户cookie
            response = jsonify({'code': code, 'message': message})
            response.set_cookie('token', '', expires=0)
            return response
        except SQLAlchemyError as e:
            # 针对数据库异常进行回滚操作
            code = 500
            message = '登出失败'
            db.session.rollback()
            logging.error(e)
            return jsonify({'code': code, 'message': message, 'error': str(e)})
        except Exception as e:
            db.session.rollback()
            code = 400
            message = "登出失败"
            return jsonify({'code': code, 'message': message, 'error': str(e)})


class Registration(Resource):
    def post(self):
        code = None
        message = None
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, required=True, location='json', help='用户名不能为空')
            parser.add_argument('password', type=str, required=True, location='json', help='密码不能为空')
            args = parser.parse_args()
            username = args['username']
            password = args['password']
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
            code = 200
            message = '注册成功'
            return jsonify({'code': code, 'message': message})
        except SQLAlchemyError as e:
            # 针对数据库异常进行回滚操作
            code = 500
            message = '注册失败'
            db.session.rollback()
            logging.error(e)
            return jsonify({'code': code, 'message': message, 'error': str(e)})
        except Exception as e:
            code = 500
            message = '注册失败'
            return jsonify({'code': code, 'message': message, 'error': str(e)})
