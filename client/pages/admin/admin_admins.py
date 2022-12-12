import os
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template
from pages.shared.get_user import *

load_dotenv()

@app.route('/admin/admins/')
def admin_admins():
    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        return render_template(
            'confirmation.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()
        

    # get users
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    users = res.json()

    admins = list(filter(lambda _user: _user['is_admin'] == True , users))
    non_admins = list(filter(lambda _user: _user['is_admin'] == False, users))


    return render_template(
        '/admin/admin-admins.html',
        user=user,
        admins=admins,
        non_admins=non_admins
    )

