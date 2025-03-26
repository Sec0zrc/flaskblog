import datetime
import logging
from . import db
from flask import current_app
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

logging.basicConfig(level=logging.DEBUG)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.set_create_time(datetime.datetime.now())

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_name(self, name):
        self.username = name

    def set_create_time(self, create_time):
        self.create_at = create_time

    def validate_password(self, password):
        flag_password_correct = None
        user = User.query.filter_by(self.username).first()
        if user:
            flag_password_correct = check_password_hash(self.password_hash, password)
        return flag_password_correct, user

    @classmethod
    def authenticate(cls, name, password):
        flag_username_exist = False
        flag_password_correct = None
        with current_app.app_context():
            try:
                user = cls.query.filter_by(username=name).first()
                if user:
                    password_hash = user.password_hash
                    flag_username_exist = True
                    flag_password_correct = check_password_hash(password_hash, password)

                return [flag_username_exist, flag_password_correct, user]
            except Exception as e:
                logging.error(e)
                return [0, 0, None]

    def check_status(self):
        if self.status == 0:
            return True
        else:
            return False


class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)

    def __init__(self, category_name):
        self.category_name = category_name

    def get_id(self, category_name):
        category = Category.query.filter_by(category_name=category_name).first()
        if category:
            return category.category_id
        else:
            return False


class Tag(db.Model):
    __tablename__ = 'tags'
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50), nullable=False)

    def __init__(self, tag_name):
        self.tag_name = tag_name

    def get_id(self, tag_name):
        tag = Tag.query.filter_by(tag_name=tag_name).first()
        if tag:
            return tag.tag_id
        else:
            # 返沪False
            return False


class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'))

    def __init__(self, title, content, user_id, category_id, tag_id):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.category_id = category_id
        self.tag_id = tag_id

    def set_create_time(self, create_time):
        self.create_at = create_time

    def set_status(self, status):
        self.status = status

    def set_content(self, content):
        self.content = content

    def set_userid(self, user_id):
        self.user_id = user_id

    def set_category_id(self, category_id):
        self.category_id = category_id

    def set_tag_id(self, tag_id):
        self.tag_id = tag_id


class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
    content = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
