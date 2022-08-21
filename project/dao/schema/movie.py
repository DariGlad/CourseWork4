from marshmallow import Schema, fields


class MovieSchema(Schema):
    """ Схема для сериализации фильмов """
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre = fields.Nested("GenreSchema")
    director = fields.Nested("DirectorSchema")
