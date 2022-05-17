from marshmallow import fields, Schema


class DirectorSchema(Schema):
    """ Описывает модель режиссера в виде класса схемы (для сериализации)."""

    id = fields.Int(required=True)
    name = fields.Str(required=True)
