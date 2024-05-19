from flask import request
from .incomeModel import db, Income, IncomeSchema
from ..utilities.response import Response
from ..user.userController import DataHandler as UserHandler


class IncomeController:
    def __init__(self, user_id):
        self.dataHandler = DataHandler()
        self.user_id = user_id

    def get_data(self):
        try:
            data = self.dataHandler.grab_data(self.user_id)
            return Response.make(status=True, data=data)
        except:
            return Response.make('Eror while trying to retrieve data')

    def insert_new_data(self):
        try:
            self.dataHandler.insert_new_data({
                'id': request.json.get('id'),
                'value': request.json.get('value'),
                'description': request.json.get('description'),
                'user_id': self.user_id,
                'date': request.json.get('date'),
                'category_id': request.json.get('category_id'),
            })
            return Response.make(True, 'Data successfully added')
        except:
            return Response.make(False, 'Insert data failed')

    def update_data(self):
        try:
            self.dataHandler.update_data({
                'id': request.json.get('id'),
                'value': request.json.get('value'),
                'description': request.json.get('description'),
                'date': request.json.get('date'),
                'category_id': request.json.get('category_id'),
            }, self.user_id)
            return Response.make(True, 'Data successfully updated')
        except:
            return Response.make(False, 'Update data failed')

    def delete_data(self):
        try:
            self.dataHandler.delete_data({
                'id': request.json.get('id'),
            }, self.user_id)
            return Response.make(True, 'Data successfully removed')
        except:
            return Response.make('Data failed to removed')

    def search_single_data(self, account_id):
        try:
            single_data = self.dataHandler.grab_single_data(account_id, self.user_id)

            if not single_data:
                return Response.make(False, 'Data not found')

            return Response.make(msg='Data Found', data=single_data)
        except:
            return Response.make(False, 'Cant find data')


class DataHandler:
    def __init__(self):
        self.Model = Income
        self.Schema = IncomeSchema

    def grab_data(self, user_id):
        if UserHandler().get_user_by_id(user_id).role.name == 'admin':
            object_results = self.Model.query.all()
        else:
            object_results = self.Model.query.filter(self.Model.user_id == user_id).all()
        return self.Schema(many=True).dump(object_results)

    def grab_single_data(self, income_id, user_id):
        if UserHandler().get_user_by_id(user_id).role.name == 'admin':
            result = self.Model.query.filter(self.Model.id == income_id).first()
        else:
            result = self.Model.query.filter(self.Model.id == income_id, self.Model.user_id == user_id).first()

        return self.Schema(many=False).dump(result)

    def grab_one(self, parameter, user_id):
        if UserHandler().get_user_by_id(user_id).role.name == 'admin':
            return self.Model.query.filter(self.Model.id == parameter.get('id')).first()
        else:
            return self.Model.query.filter(self.Model.id == parameter.get('id'), self.Model.user_id == user_id).first()

    def insert_new_data(self, parameter):
        object_to_insert = self.Model(**parameter)
        db.session.add(object_to_insert)
        db.session.commit()

    def update_data(self, data, user_id):
        income = self.grab_one(data['id'], user_id)
        income.value = data['value']
        income.description = data['description']
        income.user_id = data['user_id']
        income.date = data['date']
        income.category_id = data['category_id']
        db.session.commit()

    def delete_data(self, parameter, user_id):
        object_to_delete = self.grab_one(parameter, user_id)
        db.session.delete(object_to_delete)
        db.session.commit()
