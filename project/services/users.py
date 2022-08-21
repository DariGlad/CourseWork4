import base64
import hashlib
import hmac

from flask import current_app, abort

from project.services.base import BaseService


class UsersService(BaseService):
    """ Сервис пользователей """

    @property
    def hash_salt(self):
        return current_app.config["PWD_HASH_SALT"]

    @property
    def hash_iterations(self):
        return current_app.config["PWD_HASH_ITERATIONS"]

    def get_email(self, email):
        return self.dao.get_email(email)

    def create(self, data):
        """ Создание данных нового пользователя """

        data["password"] = self.get_hash(data["password"])
        return self.dao.create(data)

    def get_hash(self, password):
        """ Метод хеширования пароля """

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            self.hash_salt,
            self.hash_iterations
        )
        return base64.b64encode(password_hash)

    def compare_passwords(self, password_hash, password):
        """ Метод проверки хеширования паролей на идентичность(совпадение) """
        decoded_digest = base64.b64decode(password_hash)
        hash_digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            self.hash_salt,
            self.hash_iterations
        )
        return hmac.compare_digest(decoded_digest, hash_digest)

    def update_info(self, data, email):
        self.get_email(email)
        if "password" not in data.keys() and "email" not in data.keys():
            self.dao.update_info(data, email)
        else:
            abort(405)

    def update_password(self, passwords, email):
        user = self.get_email(email)
        password_old = passwords.get("old_password", None)
        password_new = passwords.get("new_password", None)
        if None not in [password_old, password_new] and self.compare_passwords(user.password, password_old):
            self.dao.update_info({"password": self.get_hash(password_new)}, email)
