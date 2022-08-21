from flask import request
from flask_restx import Namespace, Resource

from project.container import auth_service, user_service

api = Namespace('auth')


@api.route("/register/")
class RegisterView(Resource):
    """ CBV регистрации """

    @api.response(204, "Created")
    def post(self):
        json_req = request.json

        user_service.create(json_req)
        return "", 204


@api.route("/login/")
class AuthView(Resource):
    """ CBV аутентификации
     POST - получение токенов пользователя
     PUT - обновление токенов пользователя """

    def post(self):
        json_req = request.json

        email = json_req.get("email", None)
        password = json_req.get("password", None)

        if None in [email, password]:
            return "", 400

        return auth_service.generate_tokens(email, password), 200

    def put(self):
        json_req = request.json

        token = json_req.get("refresh_token")
        return auth_service.approve_refresh_token(token), 200
