from flask import render_template, Blueprint

view_routes = Blueprint('view', __name__)


@view_routes.route("/")
@view_routes.route("/index")
def hello_world():
    return render_template('index.html')


@view_routes.route('/sign-in')
def sign_in():
    return render_template('sign-in.html')


@view_routes.route('/sign-up')
def sign_up():
    print("sign -up")
    return render_template('sign-up.html')
