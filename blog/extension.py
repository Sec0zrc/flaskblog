import redis
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required

db = SQLAlchemy()
jwt = JWTManager()
redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True)


# 设置黑名单功能，实现登出功能
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return bool(redis_client.get(jti))


# # 设置token过期事件
# @jwt.expired_token_loader
# @jwt_required()
# def my_expired_token_callback(jwt_header, jwt_payload):
#     from blog.models import User
#     user_id = get_jwt_identity()
#     user = User.query.get(user_id)
#     if user:
#         user.status = 0
#         db.session.commit()
#         redis_client.sadd(jwt_payload['jti'])
#     return jsonify({"msg": "Token has expired"})
