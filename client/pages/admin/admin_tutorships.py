import json
import os
import string
from dotenv import load_dotenv
from app import app
import requests
from flask import render_template, request, redirect
from pages.shared.get_user import *


load_dotenv()

@app.route('/admin/tutorships/')
def admin_tutorships():
    # verify is admin
    user = get_user(requests)
    if user is None or "id" not in user.keys() or user['is_admin'] == False:
        session['error_message'] = 'you do not have permission to access this page'
        return redirect('/error/')
        
    # get headers
    headers = get_header()

    # param validation
    course_id = request.args.get('course_id')
    page = request.args.get('page', '1')
    size = request.args.get('size', '15')

    try:
        page = int(page)
        size = int(size)
    except:
        session['error_message'] = 'a valid page and size must be provided'
        return redirect('/error/')
    
    tutorship_params = {
        'page': page,
        'size': size
    }

    course = None
    if course_id is not None:
        if course_id.isnumeric() and int(float(course_id)) >= 0:
            tutorship_params['course_id'] = int(float(course_id))
            course_id = int(float(course_id))
        else:
            return redirect('/')

        res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/course/'), params={'id': course_id}, headers=headers)
        if res.status_code != 200:
            session['error_message'] = str(res.content)
            return redirect('/error/')
        course = res.json()

    # get tutorships
    res = requests.get(url = str(os.environ['API_ADDRESS']+'/api/tutorships/page/deep/'), params=tutorship_params, headers=headers)
    if res.status_code != 200:
        session['error_message'] = str(res.content)
        return redirect('/error/')
    tutorships = res.json()

    # pagination formatting
    tutorships_pag_headers = ['Student Name','Tutor Name','Course Title','Dept & Num','Status']
    tutorships_pag_entries = [
        {
            'url': '/admin/tutorship/?tutorship_id=' + str(tutorship['id']),
            'entries': [  
                tutorship['student']['name'],
                tutorship['tutor']['name'],
                tutorship['course']['name'],
                tutorship['course']['dept_course'],
                tutorship['status'],
            ]
        } for tutorship in tutorships
    ]

    return render_template(
        '/admin/admin-tutorships.html',
        user=user,
        # tutorships=tutorships,
        course=course,
        course_id=course_id,
        page=page,
        size=size,
        next_page="/admin/tutorships/?page=" + str(page + 1) + "&size=" + str(size),
        prev_page="/admin/tutorships/?page=" + str(page - 1) + "&size=" + str(size),
        tutorships_pag_headers=tutorships_pag_headers,
        tutorships_pag_entries=tutorships_pag_entries
    )

