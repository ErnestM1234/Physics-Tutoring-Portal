import json
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template, request
from pages.shared.get_user import *


load_dotenv()

@app.route('/admin/add-admin/confirm/', methods=['GET'])
def add_admin_confirm():

    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')

    # get headers
    headers = get_header()

    user_id = request.args.get('user_id')
    if user_id and user_id.isnumeric() and int(float(user_id)) >= 0:
        user_id = int(float(user_id))
    else:
        session['error_message'] = 'There is no provided user_id, or the user_id is invalid'
        return redirect('/error/')


    # make admin
    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/user/update/'), data=json.dumps({'is_admin': True, 'id': str(user_id)}), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')

    return redirect('/admin/admins/')


@app.route('/admin/add-admin/')
def add_admin():
    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()


    user_id = request.args.get('user_id')
    if user_id and user_id.isnumeric() and int(float(user_id)) >= 0:
        user_id = int(float(user_id))
    else:
        session['error_message'] = 'There is no provided user_id, or the user_id is invalid'
        return redirect('/error/')


    return render_template(
        '/admin/admin-add-admin.html',
        user_id=user_id,
        user=user
    )

