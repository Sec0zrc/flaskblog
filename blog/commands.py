import logging
from faker import Faker
from flask import Blueprint
from sqlalchemy import text

from blog.extension import db
from blog.models import User, Category, Tag, Post
from datetime import datetime

command_routes = Blueprint('command', __name__)

fake = Faker()
fake_logger = logging.getLogger('fake')
fake_logger.setLevel(logging.WARNING)


@command_routes.route('/initdb/<int:flag>', methods=['GET'])
def initdb(flag=0):
    """Initialize the database"""
    if flag:
        db.drop_all()
        logging.info("数据库删除成功")
    db.create_all()
    logging.info("数据库初始化成功")
    return '数据库初始化成功'


@command_routes.route('/forge', methods=['GET'])
def forge():
    """Generate fake data"""
    # 清空数据库 禁用mysql的外键检查
    db.session.execute(text('SET FOREIGN_KEY_CHECKS = 0'))
    #db.session.execute(text('PRAGMA foreign_keys = 0'))
    db.drop_all()
    db.create_all()
    logging.info("数据库初始化成功")
    # Generate admin user
    from blog.models import User
    user = User('Admin', 'test123456*a')
    user.set_create_time(datetime.now())
    # user.set_status(1)
    # add admin to db
    db.session.add(user)
    db.session.commit()
    logging.info("管理员用户添加成功")

    for _ in range(5):
        user = User(fake.name(), fake.password())
        user.set_create_time(datetime.now())
        db.session.add(user)
    db.session.commit()
    logging.info("假用户添加成功")

    # generate category
    for i in range(10):
        category = Category("category" + str(i))
        db.session.add(category)
    db.session.commit()
    logging.info("分类添加成功")

    # generate tag
    for i in range(10):
        tag = Tag(fake.name())
        db.session.add(tag)
    db.session.commit()
    logging.info("标签添加成功")

    # generate post
    for i in range(20):
        user = User.query.filter_by(username='Admin').first()
        category = Category.query.order_by(db.func.random()).first()
        tag = Tag.query.order_by(db.func.random()).first()
        post = Post(fake.sentence(), fake.paragraph(),user.user_id, category.category_id, tag.tag_id)
        post.set_create_time(datetime.now())
        post.set_status(1)
        db.session.add(post)
    db.session.commit()
    logging.info("文章添加成功")

    return "测试数据生成成功"
