from .. import db
from marshmallow import fields, Schema


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))


class RoleSchema(Schema):
    id = fields.Int(data_key='id')
    name = fields.Str(data_key='name')
