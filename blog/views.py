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


@view_routes.route('/sign-in')
def sign_in():
    return render_template('sign-in.html')


@view_routes.route('/sign-up')
def sign_up():
    print("sign -up")
    return render_template('sign-up.html')


@view_routes.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.validate_password(password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'message': str(e)}), 500


