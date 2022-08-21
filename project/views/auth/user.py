from flask import request
from flask_restx import Namespace, Resource

from project.container import auth_service, user_service, user_schema
from project.tools import auth_required

api = Namespace('user')


@api.route("/")
class UserViews(Resource):
    """
    CBV пользователя
    GET - получаем информацию пользователя
    PATCH - изменяем информацию пользователя
    """

    @auth_required
    def get(self):
        token = request.headers["Authorization"].split("Bearer ")[-1]
        data = auth_service.decode_token(token)
        email = data["email"]
        user = user_service.get_email(email)
        return user_schema.dump(user), 200

    @api.response(204, "Created")
    @auth_required
    def patch(self):
        json_req = request.json
        token = request.headers["Authorization"].split("Bearer ")[-1]
        data = auth_service.decode_token(token)
        email = data["email"]

        try:
            user_service.check_is_dict(json_req)
            user_service.update_info(json_req, email)
        except TypeError as e:
            return str(e), 400

        return "", 204


@api.route("/password/")
class PasswordViews(Resource):
    """
    CBV обновление пароля пользователя
    """

    @api.response(204, "Created")
    @auth_required
    def put(self):
        json_req = request.json
        token = request.headers["Authorization"].split("Bearer ")[-1]
        data = auth_service.decode_token(token)
        email = data["email"]

        try:
            user_service.check_is_dict(json_req)
            user_service.update_password(json_req, email)
        except TypeError as e:
            return str(e), 400

        return "", 204
