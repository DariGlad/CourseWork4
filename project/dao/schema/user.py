from marshmallow import Schema, fields


class UserSchema(Schema):
    """ Схема для сериализации пользователей """
    id = fields.Int(dump_only=True)
    email = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Int()
