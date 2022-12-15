

#-----------------------------------------------------------------------
# auth.py
# Authors: Alex Halderman, Scott Karlin, Brian Kernighan, Bob Dondero
#-----------------------------------------------------------------------

import json
import os
import urllib.request
import urllib.parse
import re
import flask
from app import app
import requests
from flask import render_template, request, redirect
from services.oit import get_basic_student

from pages.shared.get_user import *

#-----------------------------------------------------------------------

_CAS_URL = 'https://fed.princeton.edu/cas/'

#-----------------------------------------------------------------------

# Return url after stripping out the "ticket" parameter that was
# added by the CAS server.

def strip_ticket(url):
    if url is None:
        return "something is badly wrong"
    url = re.sub(r'ticket=[^&]*&?', '', url)
    url = re.sub(r'\?&?$|&$', '', url)
    return url

#-----------------------------------------------------------------------

# Validate a login ticket by contacting the CAS server. If
# valid, return the user's username; otherwise, return None.

def validate(ticket):
    val_url = (_CAS_URL + "validate" + '?service='
        + urllib.parse.quote(strip_ticket(flask.request.url))
        + '&ticket=' + urllib.parse.quote(ticket))
    lines = []
    with urllib.request.urlopen(val_url) as flo:
        lines = flo.readlines()   # Should return 2 lines.
    if len(lines) != 2:
        return None
    first_line = lines[0].decode('utf-8')
    second_line = lines[1].decode('utf-8')
    if not first_line.startswith('yes'):
        return None
    return second_line

#-----------------------------------------------------------------------

# Authenticate the remote user, and return the user's username.
# Do not return unless the user is successfully authenticated.

def authenticate():

    # If the username is in the session, then the user was
    # authenticated previously.  So return the username.
    if 'username' in flask.session:
        return flask.session.get('username')

    # If the request does not contain a login ticket, then redirect
    # the browser to the login page to get one.
    ticket = flask.request.args.get('ticket')
    if ticket is None:
        login_url = (_CAS_URL + 'login?service=' +
            urllib.parse.quote(flask.request.url))
        flask.abort(flask.redirect(login_url))

    # If the login ticket is invalid, then redirect the browser
    # to the login page to get a new one.
    username = validate(ticket)
    if username is None:
        login_url = (_CAS_URL + 'login?service='
            + urllib.parse.quote(strip_ticket(flask.request.url)))
        flask.abort(flask.redirect(login_url))

    # The user is authenticated, so store the username in
    # the session.
    username = username.strip()
    flask.session['username'] = username
    return username

#-----------------------------------------------------------------------

def _logoutapp():

    # Log out of the application.
    flask.session.clear()
    return flask.redirect('/')

#-----------------------------------------------------------------------

def _logoutcas():

    # Log out of the CAS session, and then the application.
    logout_url = (_CAS_URL + 'logout?service='
        + urllib.parse.quote(
            re.sub('logoutcas', 'logoutapp', flask.request.url)))
    flask.abort(flask.redirect(logout_url))


#-----------------------------------------------------------------------


# Routes for authentication.

@app.route('/login', methods=['GET'])
def login():
    netid = authenticate()
    encoded_jwt = jwt.encode({
            "netid": netid,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=30)
        }, os.environ['APP_SECRET_KEY'], algorithm="HS256")

    # get credential level
    user = get_user(requests)
    res = requests.post(
        url = str(os.environ['API_ADDRESS']+'/api/user-auth-id/'),
        headers={"authorization": encoded_jwt},
        data=json.dumps({"netid": netid})
    )
    user = res.json()
    # log out when failure connecting to backend 
    if res.status_code != 200:
        print('failed to get user')
        session.clear()
        return 'failed login'

    # check if user exists
    if 'id' not in user.keys():
        # get user info
        user_info = get_basic_student(netid)


        # create new user when user not found
        data = {
            "netid": netid,
            "name" : user_info["name"],
            "email": user_info["mail"],
        }
        res = requests.post(
            url = str(os.environ['API_ADDRESS']+'/api/user/create/'),
            headers={"authorization": encoded_jwt},
            data=json.dumps(data)
        )
        # log out when failure creating new user
        if res.status_code != 200:
            print('failed to create new user')
            session.clear()
        
            return 'failed login'
        print('created new user, directing to student dashboard')
        return redirect('/student/dashboard')
    else:
        # route them to correct page
        if user['is_admin'] == True:
            return redirect('/admin/dashboard')
        if user['is_tutor'] == True:
            return redirect('/tutor/dashboard')
        if user['is_student'] == True:
            return redirect('/student/dashboard')
    
        return 'Something went wrong! You are not a student!'

@app.route('/logout', methods=['GET'])
def logout():
    return redirect('/logoutcas')

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return _logoutapp()

@app.route('/logoutcas', methods=['GET'])
def logoutcas():
    return _logoutcas()
















