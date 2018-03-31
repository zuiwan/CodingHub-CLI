from marshmallow import Schema, fields, post_load

from ch.model import BaseModel


class UserSchema(Schema):
    id = fields.Str()
    name = fields.Str()

    @post_load
    def make_user(self, data):
        return User(**data)


class User(BaseModel):
    schema = UserSchema(strict=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name
