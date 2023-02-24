import os
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template
from pages.shared.get_user import *

load_dotenv()

# quick note: this displays tutorships, for some reason??
@app.route('/admin/students/')
def admin_students():

    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()
    
    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'), params={'is_student': True}, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    students = res.json()  


    return render_template(
        '/admin/admin-students.html',
        user=user,
        students=students
    )

