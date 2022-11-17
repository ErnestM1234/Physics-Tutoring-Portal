# run the following command to start the server: $ gunicorn app:app

import os
import flask 
from flask import Flask, render_template
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    # request list of users
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    data = res.json()
    print(data)
    # return 'hi'
    return render_template(
        'users.html',
        users=data
    )

@app.route('/dashboard')
def dashboard():
    # request list of users

    # res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    # data = res.json()
    # print(data)

    # return 'hi'


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
    return render_template(
        'tutordash.html', data = data
    )

@app.route('/allclasses')
def allClasses():
    # request list of users

    # res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    # data = res.json()
    # print(data)

    # return 'hi'

    
    return render_template(
        'allclasses.html'
    )

@app.route('/editbio')
def editBio():
    # request list of users

    # res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/users/'))
    # data = res.json()
    # print(data)

    # return 'hi'

    tutorbio = flask.request.args.get('tutorbio')

    return render_template(
        'editbio.html', tutorbio=tutorbio
    )