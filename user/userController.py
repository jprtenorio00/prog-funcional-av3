from datetime import datetime, timedelta
from flask import request, make_response
import jwt
import bcrypt
from .. import db, JWT_SECRETKEY
from ..utilities.response import Response
from .userModel import User


class LoginController:
    def login(self):
        user = None
        try:
            user = UserController().findUser()
        except LoginErr as msg:
            return Response.make(False, str(msg))
        except Exception:
            return Response.make(False, 'OOps, Something wrong.')

        try:
            token = self.createToken(user)
            return self.setCookie(token)
        except:
            return Response.make('Failed to create access token')

    def createToken(self, user):
        token = jwt.encode(
            payload={
                'userId': user.id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            },
            key=JWT_SECRETKEY, algorithm='HS256')
        return token

    def setCookie(self, token):
        successLogin = {'status': True, 'msg': 'Login Success'}
        response = make_response(successLogin)
        response.set_cookie('x-auth-token', token)
        return response

    def logOut(self):
        resp = make_response({'status': True, 'msg': 'Logout Success'})
        resp.delete_cookie('x-auth-token')
        return resp


class UserController:
    def insertNewData(self):
        try:
            parameter = {
                'name': request.json.get('username'),
                'password': bcrypt.hashpw(
                    request.json.get('password').encode('utf-8'),
                    bcrypt.gensalt()).decode('utf-8'),
                'role_id': 1
            }
            DataHandler().insertNewData(parameter)
            return Response.make(True, 'Data successfully added')
        except:
            return Response.make(False, 'Insert data failed')

    def findUser(self):
        parameter = {
            'name': request.json.get('username'),
        }
        user = DataHandler().getUser(parameter)
        if not user:
            raise LoginErr('User is not found')
        if bcrypt.checkpw(
                request.json.get('password').encode('utf-8'),
                user.password.encode('utf-8')
        ):
            return user
        raise LoginErr('Permission denied, your password or username is incorrect.')


class DataHandler:

    def getUser(self, parameter):
        data = User.query.filter(
            User.name == parameter.get('name')
        ).first()
        return data

    def get_user_by_id(self, user_id):
        data = User.query.filter(
            User.id == user_id
        ).first()
        return data

    def insertNewData(self, parameter):
        objectToInsert = User(**parameter)
        db.session.add(objectToInsert)
        db.session.commit()


class LoginErr(Exception):
    """Custom Exception for login error"""