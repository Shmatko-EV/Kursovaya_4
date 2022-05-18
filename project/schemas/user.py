from marshmallow import fields, Schema


class UserSchema(Schema):
    """ Описывает модель пользователя в виде класса схемы (для сериализации)."""

    id = fields.Int()
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Str()
