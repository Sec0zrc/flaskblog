import logging
from sqlalchemy.exc import SQLAlchemyError
from blog.api.users.routes import is_admin
from blog.models import Category, Post
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource, reqparse
from datetime import datetime
from blog.extension import db


class Categories(Resource):
    def get(self):
        code = None
        message = None
        data = None
        try:
            categories = Category.query.all()
            if categories:
                code = 200
                message = 'Success fetch categories'
                data = []
                for category in categories:
                    info = {'category_id': category.category_id, 'category_name': category.category_name}
                    data.append(info)
                return jsonify({'code': code, 'message': message, 'data': data})
            else:
                code = 404
                message = 'Categories not found'
                return jsonify({'code': code, 'message': message})
        except SQLAlchemyError as e:
            code = 500
            message = 'Failed to fetch categories'
            db.session.rollback()
            return jsonify({'code': code, 'message': message, 'error': str(e)}), 500
        except Exception as e:
            code = 500
            message = 'Failed to fetch categories'
            db.session.rollback()
            return jsonify({'code': code, 'message': message, 'error': str(e)}), 500

    @jwt_required()
    def post(self):
        code = None
        message = None
        # verify admin
        if not is_admin():
            code = 403
            message = 'Permission denial!'
            return jsonify({'code': code, 'message': message})
        else:
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('category_name', type=str, required=True, help='Category name is required')
                args = parser.parse_args()

                category = Category(args['category_name'])
                db.session.add(category)
                db.session.commit()
                code = 201
                message = 'Success create category'
                return jsonify({'code': code, 'message': message})
            except SQLAlchemyError as e:
                code = 500
                message = 'Failed to create category'
                db.session.rollback()
                return jsonify({'code': code, 'message': message, 'error': str(e)})
            except Exception as e:
                code = 500
                message = 'Failed to create category'
                return jsonify({'code': code, 'message': message, 'error': str(e)})

    @jwt_required()
    def delete(self, category_id):
        code = None
        message = None
        # verify admin
        if not is_admin():
            code = 403
            message = 'Permission denial!'
            return jsonify({'code': code, 'message': message})
        else:
            try:
                post = Post.query.filter_by(category_id=category_id)
                for p in post:
                    p.category_id = None
                    db.session.commit()
                category = Category.query.get(category_id)
                if category:
                    db.session.delete(category)
                    db.session.commit()
                    code = 200
                    message = 'Success delete category'
                    return jsonify({'code': code, 'message': message})
                else:
                    code = 404
                    message = 'Category not found'
                    return jsonify({'code': code, 'message': message})
            except SQLAlchemyError as e:
                code = 500
                message = 'Failed to delete category'
                db.session.rollback()
                return jsonify({'code': code, 'message': message, 'error': str(e)})
            except Exception as e:
                code = 500
                message = 'Failed to delete category'
                return jsonify({'code': code, 'message': message, 'error': str(e)})