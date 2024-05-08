from .. import db


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.DECIMAL(10, 2), default=0.0, nullable=False)
    description = db.Column(db.String(30), default='', nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='incomes')
    date = db.Column(db.Date)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='incomes')
