import calendar
import datetime

import jwt
from flask import current_app
from flask_restx import abort


class AuthService:
    """ Сервис аутентификации """

    def __init__(self, user_service):
        self.user_service = user_service

    @property
    def jwt_secret(self):
        return current_app.config["JWT_SECRET"]

    @property
    def jwt_algorithm(self):
        return current_app.config["JWT_ALGORITHM"]

    @property
    def token_expire_minutes(self):
        return current_app.config["TOKEN_EXPIRE_MINUTES"]

    @property
    def token_expire_days(self):
        return current_app.config["TOKEN_EXPIRE_DAYS"]

    def generate_tokens(self, email, password, is_refresh=False):
        """ Метод генерации токенов """

        user = self.user_service.get_email(email)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                raise abort(400)

        data = {
            "email": user.email
        }

        # Токен доступа поминутный
        minutes = datetime.datetime.utcnow() + datetime.timedelta(minutes=self.token_expire_minutes)
        data["exp"] = calendar.timegm(minutes.timetuple())
        access_token = jwt.encode(data, self.jwt_secret, algorithm=self.jwt_algorithm)

        # Токен обновления дневной
        days = datetime.datetime.utcnow() + datetime.timedelta(days=self.token_expire_days)
        data["exp"] = calendar.timegm(days.timetuple())
        refresh_token = jwt.encode(data, self.jwt_secret, algorithm=self.jwt_algorithm)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        """ Для обновления токенов """

        data = self.decode_token(refresh_token)
        email = data.get("email")
        return self.generate_tokens(email, None, is_refresh=True)

    def decode_token(self, token):
        """ Декодирование токена """

        return jwt.decode(jwt=token, key=self.jwt_secret, algorithms=[self.jwt_algorithm])
