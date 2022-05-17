from marshmallow import fields, Schema


class GenreSchema(Schema):
    """ Описывает модель жанра в виде класса схемы (для сериализации)."""

    id = fields.Int(required=True)
    name = fields.Str(required=True)
