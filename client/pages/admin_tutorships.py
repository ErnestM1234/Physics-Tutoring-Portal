import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request

load_dotenv()

@app.route('/admin/tutorships/')
def admin_tutorships():
    # param validation
    course_id = request.args.get('course_id')
    tutorship_params = {"course_id": None}
    if course_id is not None:
        if course_id.isnumeric() and int(float(course_id)) >= 0:
            tutorship_params['course_id'] = int(float(course_id))
        else:
            return redirect('/')

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is admin
    if 'id' not in user.keys() or user['is_admin'] == False:
        return redirect('/')

    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params=tutorship_params)
    tutorships = res.json()

    return render_template(
        'admin-tutorships.html',
        tutorships=tutorships
    )

