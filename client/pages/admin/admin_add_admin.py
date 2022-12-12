import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template, request
from pages.shared.get_user import *


load_dotenv()

@app.route('/admin/courses/add-admin/confirm/', methods=['GET'])
def add_admin_confirm():

    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        return render_template(
            '/admin/confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    user_id = request.args.get('user_id')
    if user_id and user_id.isnumeric() and int(float(user_id)) >= 0:
        user_id = int(float(user_id))
    else:
        return render_template(
            '/admin/confirmation.html',
            message="There is no provided user_id, or the user_id is invalid"
        )


    # make admin
    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/user/update/'), data=json.dumps({'is_admin': 'True'}), headers=headers)
    if res.status_code != 200:
        print(str(res.content))
        return render_template(
        '/admin/confirmation.html',
        message=str(res)
    )


@app.route('/admin/courses/add-admin/')
def add_admin():
    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        return render_template(
            '/admin/confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


    user_id = request.args.get('user_id')
    if user_id and user_id.isnumeric() and int(float(user_id)) >= 0:
        user_id = int(float(user_id))
    else:
        return render_template(
            '/admin/confirmation.html',
            message="There is no provided user_id, or the user_id is invalid"
        )
    
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={'id': user_id}, headers=headers)
    user = res.json()

    
    


    return render_template(
        '/admin/admin-add-admin.html',
        user_id=user_id,
        user=user
    )

