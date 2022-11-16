import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template

load_dotenv()

# quick note: this displays tutorships, for some reason??
@app.route('/admin/students/')
def admin_students():

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is admin
    if "id" not in user.keys() or user['is_admin'] == False:
        return redirect('/')
        
    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'))
    tutorships = res.json()



    return render_template(
        'admin-students.html',
        tutorships=tutorships
    )

