
import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template
import time

load_dotenv()

@app.route('/student/courses')
def student_courses():

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get student
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is student
    if "id" not in user.keys() or user['is_student'] == False:
        return redirect('/')

    # get courses
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'))
    courses = res.json()

    # Get current time in GMT
    now = time.struct_time(time.gmtime())

    # Get year
    semester = str(now[0])

    # Divide into spring/fall semester
    if now[1] < 7:
        semester = "Spring " + semester
    else:
        semester = "Fall " + semester

    return render_template(
        'student-courses.html',
        user=user,
        courses=courses,
        semester=semester
    )
