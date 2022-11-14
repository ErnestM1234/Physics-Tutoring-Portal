# run the following command to start the server: $ gunicorn app:app

import os
from flask import Flask, render_template
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    # request list of users
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    res2 = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/'))

    data = res.json()
    data2 = res2.json()
    # return 'hi'
    return render_template(
        'users.html',
        users=data,
        tutorships=data2
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
def tutorDash():
    # request list of users

    # res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    # data = res.json()
    # print(data)

    # return 'hi'
    return render_template(
        'tutordash.html'
    )