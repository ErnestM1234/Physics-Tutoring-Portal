import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request

load_dotenv()

@app.route('/admin/user/create-user/confirm', methods=['POST'])
def create_user_confirm():

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

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/user/create/'), data=json.dumps(data))
    
    message = str(res)

    return render_template(
        'confirmation.html',
        message=message
    )

@app.route('/admin/user/create-user/')
def create_user():

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is admin
    if 'id' not in user.keys() or user['is_admin'] == False:
        return redirect('/')


    return render_template(
        'create-user.html',
    )

