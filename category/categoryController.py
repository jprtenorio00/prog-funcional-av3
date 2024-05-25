from flask import request
from .categoryModel import db, Category, CategorySchema
from ..utilities.response import Response
from ..user.userController import DataHandler as UserHandler


class CategoryController:
    def __init__(self, user_id):
        self.dataHandler = DataHandler()
        self.user_id = user_id

    def get_data(self):
        try:
            data = self.dataHandler.grab_data(self.user_id)
            modified_data = map(lambda x: {**x, 'name': 'Category: ' + x['name']}, data)
            return Response.make(status=True, data=list(modified_data))
        except Exception as e:
            return Response.make(False, f"Error while trying to retrieve data: {str(e)}")

    def insert_new_data(self):
        try:
            preprocess_data = lambda data: [{k: v.strip() if isinstance(v, str) else v for k, v in item.items()} for item in [data]]
            processed_data = preprocess_data({
                'id': request.json.get('id', None), 
                'name': request.json.get('name'),
                'user_id': self.user_id,
            })

            # Verifica se os dados processados têm 'name' válido antes de inserir
            if not processed_data[0]['name']:  # Só verifica 'name' porque 'id' pode ser None
                return Response.make(False, 'Invalid data provided')

            self.dataHandler.insert_new_data(processed_data[0])
            return Response.make(True, 'Data successfully added')
        except Exception as e:
            return Response.make(False, f"Insert data failed: {str(e)}")

    def update_data(self):
        try:
            get_data = lambda x: lambda y: (x, y)
            request_data = get_data(request.json.get('id'))(request.json.get('name'))

            if not request_data[0] or not request_data[1]:
                return Response.make(False, 'Invalid data provided')

            self.dataHandler.update_data({
                'id': request_data[0],
                'name': request_data[1],
            }, self.user_id)
            return Response.make(True, 'Data successfully updated')
        except Exception as e:
            return Response.make(False, f"Update data failed: {str(e)}")

    def delete_data(self):
        try:
            self.dataHandler.delete_data({
                'id': request.json.get('category_id'),
            }, self.user_id)
            return Response.make(True, 'Data successfully removed')
        except:
            return Response.make('Data failed to removed')

    def search_single_data(self):
        try:
            single_data = grab_single_data_monad(self.dataHandler.grab_single_data, self.user_id)

            if not single_data:
                return Response.make(False, 'Data not found')

            return Response.make(msg='Data Found', data=single_data)
        except:
            return Response.make(False, 'Cant find data')


# Função monad
def grab_single_data_monad(function, parameter):
    return function(parameter) if parameter and parameter.isnumeric() else print('Invalid parameter')


class DataHandler:
    def __init__(self):
        self.Model = Category
        self.Schema = CategorySchema

    def grab_data(self, user_id):
        if UserHandler().get_user_by_id(user_id).role.name == 'admin':
            object_results = self.Model.query.all()
        else:
            object_results = self.Model.query.filter(self.Model.user_id == user_id).all()
        return self.Schema(many=True).dump(object_results)

    def insert_new_data(self, parameter):
        object_to_insert = self.Model(**parameter)
        db.session.add(object_to_insert)
        db.session.commit()

    def update_data(self, parameter, user_id):
        category = self.grab_one(parameter, user_id)
        category.id = parameter.get('id')
        category.name = parameter.get('name')
        db.session.commit()

    def delete_data(self, parameter, user_id):
        object_to_delete = self.grab_one(parameter, user_id)
        db.session.delete(object_to_delete)
        db.session.commit()

    def grab_one(self, parameter, user_id):
        if UserHandler().get_user_by_id(user_id).role.name == 'admin':
            return self.Model.query.filter(self.Model.id == parameter.get('id')).first()
        else:
            return self.Model.query.filter(self.Model.id == parameter.get('id'), self.Model.user_id == user_id).first()

    def grab_single_data(self, category_id, user_id):
        if UserHandler().get_user_by_id(user_id).role.name == 'admin':
            result = self.Model.query.filter(self.Model.id == category_id).first()
        else:
            result = self.Model.query.filter(self.Model.id == category_id, self.Model.user_id == user_id).first()
        return self.Schema(many=False).dump(result)
