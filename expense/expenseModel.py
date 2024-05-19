from .. import db
from ..category.categoryModel import CategorySchema
from marshmallow import fields, Schema


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.DECIMAL(10, 2), default=0.0, nullable=False)
    description = db.Column(db.String(30), default='', nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='expenses')
    date = db.Column(db.Date)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='expenses')


class ExpenseSchema(Schema):
    id = fields.Int(data_key='id')
    value = fields.Decimal(data_key='value')
    description = fields.Str(data_key='description')
    user_id = fields.Int(data_key='user_id')
    date = fields.Date(data_key='date')
    category_id = fields.Int(data_key='category_id')
    category = fields.Nested(CategorySchema(only=("name",)), data_key='category')
