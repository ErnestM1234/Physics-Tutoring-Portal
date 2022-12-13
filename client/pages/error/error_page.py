

from flask import render_template, session
import requests
from pages.shared.get_user import *
from app import app


# returns a user object associated with the google auth id from the session
def get_user():
    # get netid
    netid = session.get('username')
    if netid is None:
        return None
    
    # get user object
    res = requests.post(
        url = str(os.environ['API_ADDRESS']+'/api/user-auth-id/'),
        headers=get_header(),
        data=json.dumps({"netid": netid})
    )

    if res.status_code != 200:
        return None

    user = res.json()
    return user


@app.route('/error/', methods=['GET'])
def error_page():
    user = get_user()
    if user is None:
        return render_template(
            '/error/error_page.html',
            message='Your account cannot be found. Please try logging in.',
            dashboard_url=None
        )
        
    # route them to correct page
    if user['is_admin'] == True:
        dashboard_url = '/admin/dashboard'
    elif user['is_tutor'] == True:
        dashboard_url = '/tutor/dashboard'
    elif user['is_student'] == True:
        dashboard_url = '/student/dashboard'

    
    message = session.get('error_message') or 'An issue occured.'



    return render_template(
            '/error/error_page.html',
            message=message,
            dashboard_url=dashboard_url
        )
