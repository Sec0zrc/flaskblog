from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_name(self, name):
        self.username = name

    def set_status(self, status):
        self.status = status

    def set_create_time(self, create_time):
        self.create_at = create_time

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)


class Tags(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50), nullable=False)


class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'))


class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
    content = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
