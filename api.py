from flask import request
from .app import app
from .category.categoryController import CategoryController
from .income.incomeController import IncomeController
from .expense.expenseController import ExpenseController
from .user.userController import LoginController, UserController
from .utilities.auth import Auth

auth = Auth()


@app.route('/category', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth.middleware
def category(user_id):
    controller = CategoryController(user_id)
    return controller_methods(controller, request.method)


@app.get('/category/<category_id>')
@auth.middleware
def category_get_by_id(category_id, user_id):
    return CategoryController(user_id).search_single_data(category_id)


@app.route('/income', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth.middleware
def income(user_id):
    controller = IncomeController(user_id)
    return controller_methods(controller, request.method)


@app.get('/income/<income_id>')
@auth.middleware
def income_get_by_id(income_id, user_id):
    return IncomeController(user_id).search_single_data(income_id)


@app.route('/expense', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth.middleware
def expense(user_id):
    controller = ExpenseController(user_id)
    return controller_methods(controller, request.method)


@app.get('/expense/<expense_id>')
@auth.middleware
def expense_get_by_id(expense_id, user_id):
    return ExpenseController(user_id).search_single_data(expense_id)


@app.post('/login')
def login():
    return LoginController().login()


@app.get('/logout')
def log_out():
    return LoginController().logOut()


@app.post('/register')
def new_user():
    return UserController().insertNewData()


def controller_methods(controller, method):
    if method == 'POST':
        return controller.insert_new_data()
    if method == 'GET':
        return controller.get_data()
    if method == 'PUT':
        return controller.update_data()
    if method == 'DELETE':
        return controller.delete_data()
    return {'status': False, 'msg': 'ínvalid http method'}
