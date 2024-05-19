from .. import db
from marshmallow import fields, Schema


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='categories')


class CategorySchema(Schema):
    id = fields.Int(data_key='id')
    name = fields.Str(data_key='name')
    user_id = fields.Int(data_key='user_id')
