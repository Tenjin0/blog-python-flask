from marshmallow import Schema, fields


class FooSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
