
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
        session['error_message'] = 'Your session likely has expired due to inactivity. Please log in again.'
        abort(redirect('/error/'))
    
    # get user object
    res = requests.post(
        url = str(os.environ['API_ADDRESS']+'/api/user-auth-id/'),
        headers=get_header(),
        data=json.dumps({"netid": netid})
    )

    if res.status_code != 200:
        print(str(res.content))
        session['error_message'] = 'Login Failed'
        abort(redirect('/error/'))
    

    user = res.json()
    return user


def get_header():
    netid = session.get('username')
    encoded_jwt = jwt.encode({
            "netid": netid,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=30)
        }, os.environ['APP_SECRET_KEY'], algorithm="HS256")
    if netid is None:
        print('net id not found')
        session['error_message'] = 'Your session likely has expired due to inactivity. Please log in again.'
        abort(redirect('/error/'))
    return {"authorization": encoded_jwt}