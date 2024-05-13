from .. import db
from marshmallow import fields, Schema


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))


class CategorySchema(Schema):
    id = fields.Int(data_key='id')
    name = fields.Str(data_key='name')
