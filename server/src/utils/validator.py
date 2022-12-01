import json
from urllib.request import urlopen
import os

from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from authlib.jose.rfc7517.jwk import JsonWebKey
# from authlib.jose import jwt

class Auth0JWTBearerTokenValidator(JWTBearerTokenValidator):
    def __init__(self, domain, audience):
        issuer = f"https://{domain}/"
        jsonurl = urlopen(f"{issuer}.well-known/jwks.json")
        public_key = JsonWebKey.import_key_set(
            json.loads(jsonurl.read())
        )
        super(Auth0JWTBearerTokenValidator, self).__init__(
            public_key
        )
        self.claims_options = {
            "exp": {"essential": True},
            "aud": {"essential": True, "value": audience},
            "iss": {"essential": True, "value": issuer},
        }

import jwt

def decode(encoded_jwt):
    # print(encoded_jwt)
    token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ill4cVNSejVqRnZueXgyaHNMdFQ1SCJ9.eyJnaXZlbl9uYW1lIjoiRXJuZXN0IiwiZmFtaWx5X25hbWUiOiJNY0NhcnRlciIsIm5pY2tuYW1lIjoiZXJuZXN0bSIsIm5hbWUiOiJFcm5lc3QgTWNDYXJ0ZXIiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUxtNXd1MlJmTGM4bHJ4SFFLQTZtcDBKYmkxWUF2YmZiaFU5eHBlNlFNS0U9czk2LWMiLCJsb2NhbGUiOiJlbiIsInVwZGF0ZWRfYXQiOiIyMDIyLTEyLTAxVDAyOjQyOjAyLjYxOVoiLCJlbWFpbCI6ImVybmVzdG1AcHJpbmNldG9uLmVkdSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczovL2Rldi0zeHl6MThxcHRmcW9teW1xLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwODIwNDY2MzEyNzcyNjgzMDc4NiIsImF1ZCI6IjJXcVprR0lwclM3Qjc0QWI5OE4wYnh6cWV3VWtETlhUIiwiaWF0IjoxNjY5ODYyNTIzLCJleHAiOjE2Njk4OTg1MjMsInNpZCI6ImlON3VjUDRaSHJBMlFCVWJzYUVBdERMQlRrV2txQ2xuIiwibm9uY2UiOiIzWHR4c2FONmlqVTZ3NlNzd3E0RiJ9.Ev9cyv8dzQXsyXBlthgJvOEiZVgesRfQ-cbEbcndjZapCd0jSc4xUpAJ5lQDT83JyjQiWEPZEKemK8brXb6rzulpwKBSNnjZGv2tNLC5aUxjRbFfjQyN4-iumI1jN1vHllh-Q4YNEm8MLCdBhMbUL3crr_bnhYzat7ENotwxZGvizKAFF2w9NVVCRjuZo2neDjXe7gNMnhoQER5q-gKf0moJPFNjDKtRvKNAwxOqKIXXuogzcsevQGDE65bL_s2JBW4oXykRaDJkCpOCoY-Y_mhZ_iEA0kSBcsFiiBHzUiBaasxbGYYbUDxz-f8_RsdF-5scAZqbrEKfARkXYwZ_5A'
    # res = jwt.decode(encoded_jwt, key=None, algorithms=['RS256'])
    decoded = jwt.decode(token, options={"verify_signature": False})
    print(str(decoded))