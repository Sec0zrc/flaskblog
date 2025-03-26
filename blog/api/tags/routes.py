import logging
from flask import jsonify
from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError

from blog.extension import db
from blog.api.users.routes import is_admin
from blog.models import Tag
from flask_jwt_extended import jwt_required


class Tags(Resource):

    def get(self):
        code = None
        message = None

        try:
            tags = Tag.query.all()
            tags_list = []
            if tags:
                for tag in tags:
                    tags_list.append({
                        'tag_id': tag.tag_id,
                        'tag_name': tag.tag_name
                    })
                code = 200
                message = 'success'
                return jsonify({'code': code, 'message': message, 'data': tags_list})
            else:
                code = 404
                message = 'tags not found'
                return jsonify({'code': code, 'message': message})
        except Exception as e:
            code = 500
            message = 'internal server error'
            logging.error(e)
            return jsonify({'code': code, 'message': message})

    @jwt_required()
    def post(self):
        code = None
        message = None

        # check admin
        if is_admin():
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('tag_name', type=str, required=True, help='tag_name is required')
                args = parser.parse_args()

                tag_name = args['tag_name']
                if Tag.get_id(tag_name):
                    code = 409
                    message = 'tag already exists'
                    return jsonify({'code': code, 'message': message})
                else:
                    tag = Tag(tag_name)
                    db.session.add(tag)
                    db.session.commit()
                    code = 201
                    message = 'tag created'
                    return jsonify({'code': code, 'message': message})
            except SQLAlchemyError as e:
                db.session.rollback()
                code = 400
                message = 'bad request'
                logging.error(e)
                return jsonify({'code': code, 'message': message, "error": str(e)})
            except Exception as e:
                code = 500
                message = 'internal server error'
                logging.error(e)
                return jsonify({'code': code, 'message': message,"error": str(e)})
        else:
            code = 401
            message = 'unauthorized'
            return jsonify({'code': code, 'message': message})
