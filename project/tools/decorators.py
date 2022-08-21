from flask import request, abort

from project.container import auth_service


def auth_required(func):
    """ Аутентификация пользователей """

    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]

        try:
            auth_service.decode_token(token)
        except Exception as e:
            print("JWT decode exception", e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper
