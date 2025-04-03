import datetime
import logging

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
@view_routes.route("/home")
def home():
    return render_template('index.html')


@view_routes.route('/sign-in.html')
@view_routes.route('/sign-in')
def sign_in():
    return render_template('sign-in.html')


@view_routes.route('/sign-up.html')
@view_routes.route('/sign-up')
def sign_up():
    print("sign -up")
    return render_template('sign-up.html')


@view_routes.route('/login.html')
@view_routes.route('/login')
def login():
    print("login page")
    return render_template('login.html')


@view_routes.route('/logout.html')
@view_routes.route('/logout')
def logout():
    print("logout page")
    return render_template('logout.html')


@view_routes.route('/dashboard.html')
@view_routes.route('/dashboard')
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    user_ip = request.remote_addr
    current_time = datetime.datetime.now()
    return render_template('dashboard.html', user_ip=user_ip, current_time=current_time)


@view_routes.route('/dashboard-posts.html')
@view_routes.route('/dashboard-posts')
@jwt_required()
def dashboard_post():
    return render_template('dashboard-posts.html')


@view_routes.route('/posts.html')
@view_routes.route('/posts')
def posts():
    return render_template('posts.html')
