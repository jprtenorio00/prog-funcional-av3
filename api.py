from flask import request
from .app import app
from .category.categoryController import CategoryController


@app.route('/category_api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def category_api():
    controller = CategoryController()
    if request.method == 'POST':
        return controller.insert_new_data()
    if request.method == 'GET':
        return controller.get_data()
    if request.method == 'PUT':
        return controller.update_data()
    if request.method == 'DELETE':
        return controller.delete_data()
    return {'status': False, 'msg': 'ínvalid http method'}


@app.get('/category_api_search/<category_id>')
def category_api_search(category_id):
    return CategoryController().search_single_data(category_id)

