from flask import request
from .categoryModel import db, Category, CategorySchema
from ..utilities.response import Response


class CategoryController:
    def __init__(self):
        self.dataHandler = DataHandler()

    def get_data(self):
        try:
            data = self.dataHandler.grab_data()
            return Response.make(status=True, data=data)
        except:
            return Response.make('Eror while trying to retrieve data')

    def insert_new_data(self):
        try:
            self.dataHandler.insert_new_data({
                'id': request.json.get('id'),
                'name': request.json.get('name'),
            })
            return Response.make(True, 'Data successfully added')
        except:
            return Response.make(False, 'Insert data failed')

    def update_data(self):
        try:
            self.dataHandler.update_data({
                'id': request.json.get('id'),
                'name': request.json.get('name'),
            })
            return Response.make(True, 'Data successfully updated')
        except:
            return Response.make(False, 'Update data failed')

    def delete_data(self):
        try:
            self.dataHandler.delete_data({
                'id': request.json.get('category_id'),
            })
            return Response.make(True, 'Data successfully removed')
        except:
            return Response.make('Data failed to removed')

    def search_single_data(self, account_id):
        try:
            single_data = self.dataHandler.grab_single_data_monad(account_id)

            if not single_data:
                return Response.make(False, 'Data not found')

            return Response.make(msg='Data Found', data=single_data)
        except:
            return Response.make(False, 'Cant find data')


class DataHandler:
    def __init__(self):
        self.Model = Category
        self.Schema = CategorySchema

    def grab_data(self):
        object_results = self.Model.query.all()
        return self.Schema(many=True).dump(object_results)

    def insert_new_data(self, parameter):
        object_to_insert = self.Model(**parameter)
        db.session.add(object_to_insert)
        db.session.commit()

    def update_data(self, parameter):
        category = self.grab_one(parameter)
        category.id = parameter.get('id')
        category.name = parameter.get('name')
        db.session.commit()

    def delete_data(self, parameter):
        object_to_delete = self.grab_one(parameter)
        db.session.delete(object_to_delete)
        db.session.commit()

    def grab_one(self, parameter):
        return self.Model.query.filter(self.Model.id == parameter.get('id')).first()

    def grab_single_data_monad(self, parameter):
        return self.grab_single_data(parameter) if parameter and parameter.isnumeric() else print('Invalid parameter')

    def grab_single_data(self, parameter):
        result = self.Model.query.filter(self.Model.id == parameter).first()
        return self.Schema(many=False).dump(result)
