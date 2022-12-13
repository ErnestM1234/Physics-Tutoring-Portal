

from flask import render_template, session
from pages.shared.get_user import *
from app import app


@app.route('/error/', methods=['GET'])
def error_page():
    message = session.get('error_message') or 'An issue occured.'
    return render_template(
            '/error/error_page.html',
            message=message
        )
