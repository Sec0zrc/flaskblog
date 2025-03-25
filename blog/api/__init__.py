from flask import Blueprint
from flask_restful import Api

# 创建api蓝图对象
api_bp = Blueprint('api', __name__)

# 创建flask_restful的api实例
api = Api(api_bp)

# # 导入子模块的路由或资源
from .auth.routes import AuthLogin, AuthLogout
from .users.routes import Users
from .posts.routes import Posts
from .categories.routes import Categories

api.add_resource(AuthLogin, '/auth/login')
api.add_resource(AuthLogout, '/auth/logout')
api.add_resource(Users, '/users', '/users/<int:user_id>')
api.add_resource(Posts, '/posts', '/posts/<int:post_id>')
api.add_resource(Categories, '/categories', '/categories/<int:category_id>')