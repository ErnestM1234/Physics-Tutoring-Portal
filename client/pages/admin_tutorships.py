import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template

load_dotenv()

@app.route('/admin/courses/<course_id>/tutorships')
def admin_tutorships(course_id):

    # param validation
    if course_id.isnumeric() and int(float(course_id)) >= 0:
        validated_course_id = int(float(course_id))
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
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={"course_id": validated_course_id})
    tutorships = res.json()

    return render_template(
        'admin-tutorships.html',
        tutorships=tutorships
    )

