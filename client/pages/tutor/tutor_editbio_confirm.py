import os
from dotenv import load_dotenv
from app import app
import requests
from flask import redirect, render_template, request
from pages.shared.get_user import *

load_dotenv()

@app.route('/tutor/editbio/confirm', methods=['POST'])
def edit_bio_confirm():
    # verify is tutor
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_tutor'] == False:
        return render_template(
            '/tutor/tutor-no-access.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()

    bio = request.form.get('bio')
    if bio is None:
        return redirect('/tutor/editbio.html')

   
    data = {
        'bio': bio,
        'id': user['id']
    }

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/user/update/'), data=json.dumps(data), headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    message = str(res)


    return render_template(
        '/tutor/tutor-confirmation.html',
        message=message, 
        user=user
    )