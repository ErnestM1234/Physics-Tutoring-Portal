# run the following command to start the server: $ gunicorn app:app

import os
from flask import Flask, render_template, redirect
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    # todo: should this autoroute to one of the three dashboards??

    # request list of users
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    res2 = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'))
    res3 = requests.get(url = str(os.environ['API_ADDRESS']+'/api/courses/'))

    data = res.json()
    data2 = res2.json()
    data3 = res3.json()
    # return 'hi'
    return render_template(
        'users.html',
        users=data,
        tutorships=data2,
        courses=data3
    )

@app.route('/dashboard')
def dashboard():
    # request list of users

    # res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    # data = res.json()
    # print(data)

    # return 'hi'

    #student_netid = "lglisic"
    #student_id = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'), params={'student_id':"NAME"})

    #student_id = 1

    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    data = res.json()

    names=[]
    netids=[]
    emails=[]

    for user in data:
        names.append(user['name'])
        netids.append(user['netid'])
        emails.append(user['email'])

    data = zip(names, netids, emails)

    # get tutors


    #res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'), params={'student_id': student_id})

    return render_template(
        'dashboard.html',
        data = data

    )

@app.route('/tutordashboard')
def tutor_dashboard():
    # request list of users

    # res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    # data = res.json()
    # print(data)

    # return 'hi'
    return render_template(
        'tutordash.html'
    )


# pylint: disable-next=unused-import
# pylint: disable-next=wrong-import-position
# pylint: disable-next=unused-wildcard-import
# pylint: disable-next=wildcard-import
from pages.admin_dashboard import *
from pages.admin_courses import *
from pages.admin_tutorships import *
from pages.admin_tutors import *
from pages.admin_students import *
from pages.admin_admins import *
from pages.create_course import *
from pages.create_tutor_course import *
from pages.create_tutorship import *


if __name__ == '__main__':
    app.run()
