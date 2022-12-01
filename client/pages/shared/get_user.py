
import json
from flask import session, render_template
import os

# returns a user object associated with the google auth id from the session
def get_user(requests):


    # get google auth id
    token = session.get('user')
    if token is None:
        print('no token')
        return None
    user_info = token['userinfo']
    if user_info is None or user_info['sub'] is None or user_info['sub'] is '':
        print('token info was not resolved')
        return None
    auth_id = user_info['sub']
    
    # get user object
    res = requests.post(
        url = str(os.environ['API_ADDRESS']+'/api/user-auth-id/'),
        headers={"authorization": "Bearer " + token["id_token"]},
        data=json.dumps({"auth_id": auth_id})
    )
    user = res.json()

    if res.status_code != 200:
        print(str(res.content))
        return None
    return user


def get_header():
    token = session.get('user')
    if token is None:
        return None
    return {"authorization": "Bearer " + token["id_token"]}