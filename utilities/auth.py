from .response import Response
from flask import request
from functools import wraps
import jwt
from .. import JWT_SECRETKEY


class Auth:
    user_id = None

    def middleware(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            token = request.cookies.get('x-auth-token')
            if not token:
                return Response.make(False, 'Forbidden access')
            try:
                self.user_id = jwt.decode(token, JWT_SECRETKEY, algorithms='HS256').get('userId')
                print(self.user_id)
            except jwt.ExpiredSignatureError:
                return Response.make(False, 'Unauthorized')
            except jwt.InvalidTokenError:
                return Response.make(False, 'Invalid token')
            return func(*args, **kwargs, user_id=self.user_id)

        return decorator
