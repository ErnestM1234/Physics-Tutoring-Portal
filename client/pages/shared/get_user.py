
import json
from flask import session, abort, redirect
import os

# returns a user object associated with the google auth id from the session
def get_user(requests):
    # get netid
    netid = session.get('username')
    if netid is None:
        abort(redirect('/error/?message=' + res.content))
    
    # get user object
    res = requests.post(
        url = str(os.environ['API_ADDRESS']+'/api/user-auth-id/'),
        headers=get_header(),
        data=json.dumps({"netid": netid})
    )
    user = res.json()

    if res.status_code != 200:
        print(str(res.content))
        abort(redirect('/error/?message=' + res.content))
    return user


def get_header():
    netid = session.get('username')
    if netid is None:
       abort(redirect('/error/?message=netid-missing'))
    return {"authorization": netid}