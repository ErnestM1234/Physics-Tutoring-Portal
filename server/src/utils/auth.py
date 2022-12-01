
import json
from six.moves.urllib.request import urlopen
from functools import wraps

from flask import Flask, request, jsonify, _request_ctx_stack
# from jose import jwt
# from authlib.jose import jwt
from app import app, context

import jwt



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
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

def requires_auth(f):
    """Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            if (payload['sub'] is not None and payload['sub'] != ''):
                context['auth_id'] = payload['sub']
            else:
                raise AuthError({"code": "invalid_header",
                            "description":
                                "Cannot find payload['sub'] in"
                                " token."}, 401)

        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                            "description": "token is expired"}, 401)
        # except jwt.JWTClaimsError:
        #     raise AuthError({"code": "invalid_claims",
        #                     "description":
        #                         "incorrect claims,"
        #                         "please check the audience and issuer"}, 401)
        except Exception as e:
            print(str(e))
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Unable to parse authentication"
                                " token."}, 401)

        _request_ctx_stack.top.current_user = payload
        return f(*args, **kwargs)
    return decorated