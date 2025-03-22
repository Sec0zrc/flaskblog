from flask import Flask
from sqlalchemy import text

from blog.extension import db, jwt
from blog import models
from blog.config import Config
import click


# 工厂函数注册app对象
def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 配置数据库URI
    app.config['SQLALCHEMY_DATABASE_URI'] = config_class.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 初始化SQLAlchemy
    db.init_app(app)

    # 初始化jwt
    jwt.init_app(app)
    # 工厂类函数注册app对象
    # 延迟注册 确保api_bp已初始化
    with app.app_context():
        # 初始化数据库对象
        db.create_all()
        # 注册api资源蓝图
        from blog.api import api_bp
        app.register_blueprint(api_bp, url_prefix='/api/v1')
        from blog.commands import command_routes
        from blog.views import view_routes
        app.register_blueprint(command_routes, url_prefix='/')
        app.register_blueprint(view_routes, url_prefix='/')

    return app


if __name__ == '__main__':
    app = create_app(Config)
    print(app.url_map)

    @app.route('/test_db')
    def test_db():
        try:
            db.session.execute(text('SELECT 1'))
            return '<h1>Database connection is successful!</h1>'
        except Exception as e:
            return f'<h1>Error: {str(e)}</h1>'


    app.run(host='0.0.0.0', port=5000, debug=True)
