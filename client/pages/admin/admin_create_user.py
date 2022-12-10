import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template, request, redirect
from pages.shared.get_user import *


load_dotenv()

@app.route('/admin/user/create-user/confirm', methods=['POST'])
def create_user_confirm():

    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        return render_template(
            '/admin/confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    netid = request.form.get('netid')
    name = request.form.get('name')
    email = request.form.get('email')
    bio = request.form.get('bio')
    is_student = request.form.get('is_student')
    is_tutor = request.form.get('is_tutor')
    is_admin = request.form.get('is_admin')

    if netid is None or name is None or email is None:
        return redirect('/')

    
    data = {
        'netid': netid,
        'name': name,
        'email': email,
        'bio': bio,
        'is_student': is_student == 'on',
        'is_tutor': is_tutor == 'on',
        'is_admin': is_admin == 'on'
    }

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/user/create/'), data=json.dumps(data), headers=headers)
    
    message = str(res)

    return render_template(
        '/admin/confirmation.html',
        message=message
    )

@app.route('/admin/user/create-user/')
def create_user():

    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        return render_template(
            '/admin/confirmation.html',
            message='you do not have permission to access this page'
        )


    return render_template(
        '/admin/admin-create-user.html',
    )

