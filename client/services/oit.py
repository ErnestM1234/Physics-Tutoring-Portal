import base64
import json
import os
import requests
import flask


def get_access_token():
    REFRESH_TOKEN_URL = 'https://api.princeton.edu:443/token'

    CONSUMER_KEY = str(os.environ['OIT_CONSUMER_KEY'])
    CONSUMER_SECRET = str(os.environ['OIT_CONSUMER_SECRET'])

    req = requests.post(
        REFRESH_TOKEN_URL,
        data={"grant_type": "client_credentials"},
        headers={
            "Authorization": "Basic " + base64.b64encode(bytes(CONSUMER_KEY + ":" + CONSUMER_SECRET, "utf-8")).decode("utf-8")
        },
    )

    text = req.text
    response = json.loads(text)
    return response["access_token"]


def get_basic_student(netid):
    BASE_URL = 'https://api.princeton.edu:443/active-directory/1.0.5'
    ENDPOINT = '/users/basic'

    access_token = get_access_token()


    req = requests.get(
        BASE_URL + ENDPOINT + "?uid=" + netid,
        headers={
            "Authorization": "Bearer " + access_token
        },
    )

    if req.status_code != 200:
        print('failed to get user bio')
        flask.session.clear()
        flask.abort(flask.redirect('/logout'))

    text = req.text
    response = json.loads(text)[0]


    return {"name": response["displayname"], "mail": response["mail"]}