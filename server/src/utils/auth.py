from functools import wraps
import os
import jwt
from flask import request, jsonify
from app import app, context
from src.database.models import Users

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
    encoded_jwt = request.headers.get("authorization", None)
    try:
        auth = jwt.decode(encoded_jwt, os.environ['APP_SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError as e:
        print(str(e))
        raise AuthError({"code": "cannot_parse_authorization_header",
                        "description":
                            "Authorization header expired"}, 401)

    except Exception as e:
        print(str(e))
        raise AuthError({"code": "cannot_parse_authorization_header",
                        "description":
                            "Authorization header could not be parsed"}, 401)

    if not auth \
        or "netid" not in auth.keys() \
        or not auth['netid'] \
        or auth['netid'] == '':
        raise AuthError({"code": "authorization_missing",
                        "description":
                            "Authorization header is expected"}, 401)
    return auth['netid']

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        netid = get_auth_netid()
        try:
            user = Users.query.filter(Users.netid == netid).first()
            context['user'] = user
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