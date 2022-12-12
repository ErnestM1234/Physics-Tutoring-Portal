

from flask import render_template, request
from pages.shared.get_user import *
from app import app
from flask import render_template, request
import requests


@app.route('/error/', methods=['GET'])
def error_page():
    message = request.args.get('message') or 'An issue occured.'

    return render_template(
            '/error/error_page.html',
            message=message
        )
