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
            'tutor-no-access.html',
            message='you do not have permission to access this page'
        )
    # get headers
    headers = get_header()


    bio = request.form.get('bio')

    if bio is None:
        return redirect('/editbio')

   
    data = {
        'bio': bio,
        'id': user['id']
    }

    res = requests.post(url = str(os.environ['API_ADDRESS']+'/api/user/update/'), data=json.dumps(data), headers=headers)
   
    message = str(res)


    return render_template(
        'confirmationtutor.html',
        message=message
    )