import json
from app import app, db, context
from flask import jsonify, request
from src.utils.auth import requires_auth
from src.database.models import Tutorships, TutorCourses, Users, Courses
from marshmallow import Schema, fields
from src.services.gmail_service.gmail_service import send_tutorship_request_email, send_tutorship_accept_email, send_tutorship_deny_email


""" POST /api/tutorship/request-all/
Parameters:
    - status        (string)?
    - student_id    (int)!
    - course_id     (int)!
"""
class TutorshipRequestAllInputSchema(Schema):
    status = fields.String(required=False)
    student_id = fields.Integer(required=True)
    course_id = fields.Integer(required=True)
tutorship_request_all_input_schema = TutorshipRequestAllInputSchema()

@app.route('/api/tutorship/request-all/', methods=['POST'])
@requires_auth
def tutorship_request_all():
    data = json.loads(request.data)
    errors = tutorship_request_all_input_schema.validate(data)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400
    
    try:
        # get access_level
        user = context['user']
        if user is None:
            return {"message": "User could not be found."}, 400
        access_level = None
        if user.is_admin: access_level = "ADMIN"
        elif user.is_tutor: access_level = "TUTOR"
        elif user.is_student: access_level = "STUDENT"

        status = data.get('status', None)
        student_id = data.get('student_id')
        course_id = data.get('course_id')

        # only admin can perform mass actions
        if access_level != "ADMIN":

            # only acception is request all
            if status != "REQUESTED":
                return {"error": "Unauthorized"}, 401
        
            # student id must belong to the person sending the request
            if user.id != student_id:
                return {"error": "Unauthorized"}, 401


        # get the student and check that student_id is a student
        filters = []
        filters.append(Users.id == student_id)
        filters.append(Users.is_student == True)
        student = Users.query.filter(*filters).first()
        if student is None:
            return {"message": "Given student id must be a student."}, 400
        
        # get the course
        filters = []
        filters.append(Courses.id == course_id)
        course = Courses.query.filter(*filters).first()
        if course is None:
            return {"message": "The given course does not exist."}, 400

        # only get the approved tutor courses
        filters = []
        filters.append(TutorCourses.course_id == course_id)
        filters.append(TutorCourses.status == 'ACCEPTED') # in this case, must be available (not unavailable)
        tutor_courses = TutorCourses.query.filter(*filters).all()
        if tutor_courses is None or tutor_courses == []:
            return {"message": "There are no tutors to request here."}, 400
        tutor_ids = [tutor_course.tutor_id for tutor_course in tutor_courses]

        # Prevent duplicate tutorships (where student, tutor, and course repeat):
        # (1) find any duplicate tutorships
        filters = []
        filters.append(Tutorships.student_id == student_id)
        filters.append(Tutorships.course_id == course_id)
        duplicate_tutorship = Tutorships.query.filter(*filters).all()
        dupllicate_tutorship_tutor_ids = [int(tutorship.tutor_id) for tutorship in duplicate_tutorship]
        # (2) remove any tutor_ids that already belong to these duplicate tutorships
        tutor_ids = [tutor_id for tutor_id in tutor_ids if tutor_id not in dupllicate_tutorship_tutor_ids]
        if len(tutor_ids) == 0:
            return {"message": "There are no more tutors left for you to apply to in this course."}, 400

        # get the (elidgible) tutors
        filters = []
        filters.append(Users.id.in_(tutor_ids))
        filters.append(Users.is_tutor == True)
        tutors = Users.query.filter(*filters).all()
        if tutors is None or tutors == []:
            return {"message": "No tutors were found."}, 400
        
        # create tutorships in database
        for tutor_id in tutor_ids:
            tutorship = Tutorships(status, student_id, tutor_id, course_id)
            db.session.add(tutorship)
        db.session.commit()

        # send email notification
        tutors = [tutor.serialize() for tutor in tutors]
        student = student.serialize()
        course = course.serialize()
        if status != None:
            try:
                for tutor in tutors:
                    if status == 'REQUESTED':
                        send_tutorship_request_email(tutor['email'], student['name'], course['name'])
                    elif status == 'ACCEPTED':
                        send_tutorship_accept_email(student['email'], tutor['name'], course['name'])
                    elif status == 'REJECTED':
                        send_tutorship_deny_email(student['email'], tutor['name'], course['name'])
            except Exception as e:
                print("email sending failed: " + str(e))

        return {"message": "success" }, 200
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400

