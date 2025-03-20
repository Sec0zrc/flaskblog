import os
import sys
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_login import LoginManager

# 工厂函数注册app对象

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    # 配置数据库URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/blog'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 初始化SQLAlchemy
    db.init_app(app)

    # 工厂类函数注册app对象
    # 延迟注册
    with app.app_context():
        from app.commands import command_routes
        from app.views import view_routes
        app.register_blueprint(command_routes, url_prefix='/')
        app.register_blueprint(view_routes, url_prefix='/')
    return app




if __name__ == '__main__':
    app = create_app()
    print(app.url_map)
    app.run(host='0.0.0.0', port=5000, debug=True)
    from app import views, errors, commands
