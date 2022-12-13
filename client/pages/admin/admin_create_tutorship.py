import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template, request, redirect
from pages.shared.get_user import *


load_dotenv()

@app.route('/admin/tutorships/create-tutorship/confirm', methods=['POST'])
def create_tutorship_confirm():

    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()

    student_id = request.form.get('student_id')
    tutor_id = request.form.get('tutor_id')
    course_id = request.form.get('course_id')
    status = request.form.get('status')

    if student_id is None or tutor_id is None or course_id is None or status is None:
        return redirect('/')

    
    data = {
        'student_id': student_id,
        'tutor_id': tutor_id,
        'course_id': course_id,
        'status': status,
    }

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/tutorship/create/'), data=json.dumps(data), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')

    return redirect('/admin/tutorships/')

@app.route('/admin/tutorships/create-tutorship/')
def create_tutorship():

   # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        

    return render_template(
        '/admin/admin-create-tutorship.html',
    )

