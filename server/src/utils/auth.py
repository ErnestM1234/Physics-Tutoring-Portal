
import json
from functools import wraps

from flask import Flask, request, jsonify, _request_ctx_stack
# from jose import jwt
# from authlib.jose import jwt
from app import app, context, db

import jwt

from src.database.models import Users



AUTH0_DOMAIN = 'dev-3xyz18qptfqomymq.us.auth0.com'
API_AUDIENCE = 'http://localhost:3000' # identifier
ALGORITHMS = ["RS256"]

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

# Format error response and append status code
def get_auth_netid():
    """Obtains the netid from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth or auth == "":
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)
    return auth

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        netid = get_auth_netid()
        try:
            user = Users.query.filter(Users.netid == netid).first()
        except Exception as e:
            print(str(e))
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Unable to parse authentication"
                                " token."}, 401)
        if not user:
            context['netid'] = netid

        return f(*args, **kwargs)
    return decorated