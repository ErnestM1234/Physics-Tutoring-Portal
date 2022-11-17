import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template

load_dotenv()

@app.route('/admin/admins/')
def admin_admins():

    # this is temporary, this will be given to us by CAS or smth
    userId = 1
    
    # get admin
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/user/'), params={"id": userId})
    user = res.json()
    # verify is admin
    if "id" not in user.keys() or user['is_admin'] == False:
        return redirect('/')
        

    # get users
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    users = res.json()

    admins = list(filter(lambda user: user['is_admin'] == True and user['id'] != userId, users))
    non_admins = list(filter(lambda user: user['is_admin'] == False, users))


    return render_template(
        'admin-admins.html',
        admins=admins,
        non_admins=non_admins
    )

