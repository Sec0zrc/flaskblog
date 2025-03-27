from flask import render_template, Blueprint, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required
)

from blog.models import User

view_routes = Blueprint('view', __name__)


@view_routes.route("/")
@view_routes.route("/index")
def home():
    return render_template('index.html')


@view_routes.route('/sign-in.html')
def sign_in():
    return render_template('sign-in.html')


@view_routes.route('/sign-up.html')
def sign_up():
    print("sign -up")
    return render_template('sign-up.html')


@view_routes.route('/login.html')
def login():
    print("login page")
    return render_template('login.html')


@view_routes.route('/logout.html')
def logout():
    print("logout page")
    return render_template('logout.html')


@view_routes.route('/dashboard.html')
@jwt_required()
def dashboard():
    return render_template('dashboard.html')

@view_routes.route('/posts.html')
def posts():
    return render_template('posts.html')
