
import datetime
import json
from flask import session, abort, redirect
import os
import jwt

# returns a user object associated with the google auth id from the session
def get_user(requests):
    # get netid
    netid = session.get('username')
    if netid is None:
        abort(redirect('/error/?message=' + str(res.content)))
    
    # get user object
    res = requests.post(
        url = str(os.environ['API_ADDRESS']+'/api/user-auth-id/'),
        headers=get_header(),
        data=json.dumps({"netid": netid})
    )
    user = res.json()

    if res.status_code != 200:
        print(str(res.content))
        abort(redirect('/error/?message=' + str(res.content)))
    return user


def get_header():
    netid = session.get('username')
    encoded_jwt = jwt.encode({
            "netid": netid,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=30)
        }, os.environ['APP_SECRET_KEY'], algorithm="HS256")
    if netid is None:
       abort(redirect('/error/?message=netid-missing'))
    return {"authorization": encoded_jwt}