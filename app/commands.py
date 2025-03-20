import click
from flask import request, url_for, redirect, flash, jsonify, Blueprint
from app.models import Users, Categories, Posts, Comments, Tags
from app import db
command_routes = Blueprint('command', __name__)


@command_routes.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@command_routes.cli.command()
def forge():
    """Generate fake data"""
    db.create_all()
    click.echo('Generating the fake data...')
    # Generate admin user
    user = Users()
    user.set_name('Admin')
    user.set_password('test123456*a')
    user.set_create_time('2025-01-01 00:00:00')
    user.set_status(1)
    # add admin to db
    db.session.add(user)
    db.session.commit()
    click.echo('add amdin to db')


@command_routes.route('/api/v1/users', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        # 获取用户列表
        users = Users.query.all()
        user_list = [
            {'user_id': user.user_id, 'username': user.username, 'create_at': user.create_at, 'status': user.status} for
            user in users]
        return jsonify(user_list)
    else:
        # 添加用户
        username = request.form.get('username')
        password = request.form.get('password')
        status = request.form.get('status')
        create_at = request.form.get('create_at')
        user = Users()
        user.set_name(username)
        user.set_password(password)
        user.set_create_time(create_at)
        user.set_status(status)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Success create user'}), 201
