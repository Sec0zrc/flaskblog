import logging

import pytest
from flask_sqlalchemy import SQLAlchemy

from blog import create_app
from blog.config import TestConfig
from blog.extension import db
from blog.commands import forge


@pytest.fixture(scope='module')
def test_client():
    # 创建测试用的flask app
    app = create_app(config_class=TestConfig)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as test_client:
        with app.app_context():
            # 初始化测试数据库
            forge()
            logging.info("forge success")
            yield test_client
            db.drop_all()

