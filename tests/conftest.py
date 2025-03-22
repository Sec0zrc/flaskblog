import pytest
from blog import create_app
from blog.config import TestConfig
from blog.extension import db
from blog.commands import forge


@pytest.fixture(scope='module')
def test_client():
    # 创建测试用的flask app
    app = create_app(config_class=TestConfig)
    print(TestConfig.SQLALCHEMY_DATABASE_URI)
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        with app.app_context():
            # 初始化测试数据库
            forge()
            yield test_client
            db.drop_all()
