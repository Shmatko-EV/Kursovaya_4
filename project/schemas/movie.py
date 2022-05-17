from marshmallow import fields, Schema


class MovieSchema(Schema):
    """ Описывает модель фильма в виде класса схемы (для сериализации)."""

    id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
