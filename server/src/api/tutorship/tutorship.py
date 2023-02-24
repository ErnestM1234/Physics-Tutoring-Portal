import json
from app import app, db
from flask import jsonify, request
from src.utils.auth import requires_auth
from src.database.models import Tutorships, TutorCourses, Users, Courses
from marshmallow import Schema, fields
from src.services.gmail_service.gmail_service import send_tutorship_request_email, send_tutorship_accept_email, send_tutorship_deny_email


""" GET /api/tutorship/
Parameters:
    - id (int)!
"""
class GetTutorshipInputSchema(Schema):
    id = fields.Integer(required=True)
get_tutorship_input_schema = GetTutorshipInputSchema()

@app.route('/api/tutorship/', methods=['GET'])
@requires_auth
def get_tutorship():
    errors = get_tutorship_input_schema.validate(request.args)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400
    
    try:
        id = request.args.get('id')
        tutorship = Tutorships.query.filter(Tutorships.id == id).first()
        if tutorship is None:
            return {"message": "Tutorship could not be found."}, 400
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400

    return jsonify(tutorship.serialize())




""" GET /api/tutorships/
Parameters:
    - id            (int)?
    - status        (str)?
    - student_id    (int)?
    - tutor_id      (int)?
    - course_id      (int)?
"""
class GetTutorshipsInputSchema(Schema):
    id = fields.Integer()
    status = fields.String()
    student_id = fields.Integer()
    tutor_id = fields.Integer()
    course_id = fields.Integer()
get_tutorships_input_schema = GetTutorshipsInputSchema()

@app.route('/api/tutorships/', methods=['GET'])
@requires_auth
def get_tutorships():
    errors = get_tutorships_input_schema.validate(request.args)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400
    
    try:
        id = request.args.get('id')
        status = request.args.get('status')
        student_id = request.args.get('student_id')
        tutor_id = request.args.get('tutor_id')
        course_id = request.args.get('course_id')

        filters = []
        if id:
            filters.append(Tutorships.id == id)
        if status:
            filters.append(Tutorships.status == status)
        if student_id:
            filters.append(Tutorships.student_id == student_id)
        if tutor_id:
            filters.append(Tutorships.tutor_id == tutor_id)
        if course_id:
            filters.append(Tutorships.course_id == course_id)

        tutorships = Tutorships.query.filter(*filters).all()
        return jsonify([tutorship.serialize() for tutorship in tutorships])
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400






""" GET /api/tutorships/deep/
Parameters:
    - id            (int)?
    - status        (str)?
    - student_id    (int)?
    - tutor_id      (int)?
    - course_id      (int)?
"""
class GetTutorshipsDeepInputSchema(Schema):
    id = fields.Integer()
    status = fields.String()
    student_id = fields.Integer()
    tutor_id = fields.Integer()
    course_id = fields.Integer()
get_tutorships_deep_input_schema = GetTutorshipsDeepInputSchema()

@app.route('/api/tutorships/deep/', methods=['GET'])
@requires_auth
def get_tutorships_deep():
    errors = get_tutorships_deep_input_schema.validate(request.args)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400
    
    try:
        id = request.args.get('id')
        status = request.args.get('status')
        student_id = request.args.get('student_id')
        tutor_id = request.args.get('tutor_id')
        course_id = request.args.get('course_id')

        filters = []
        if id:
            filters.append(Tutorships.id == id)
        if status:
            filters.append(Tutorships.status == status)
        if student_id:
            filters.append(Tutorships.student_id == student_id)
        if tutor_id:
            filters.append(Tutorships.tutor_id == tutor_id)
        if course_id:
            filters.append(Tutorships.course_id == course_id)

        tutorships = Tutorships.query.filter(*filters).all()
        tutorships = [tutorship.serialize() for tutorship in tutorships]

        # get the courses and tutors and students
        for tutorship in tutorships:
            tutor = Users.query.filter(Users.id == tutorship["tutor_id"]).first()
            if tutor:
                tutorship["tutor"] = tutor.serialize()
            student = Users.query.filter(Users.id == tutorship["student_id"]).first()
            if student:
                tutorship["student"] = student.serialize()
            course = Courses.query.filter(Courses.id == tutorship["course_id"]).first()
            if course:
                tutorship["course"] = course.serialize()

        return jsonify(tutorships)
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400





""" GET /api/tutorships/count/
Parameters:
    - id            (int)?
    - status        (str)?
    - student_id    (int)?
    - tutor_id      (int)?
    - course_id     (int)?
"""
class GetTutorshipsCountInputSchema(Schema):
    id = fields.Integer()
    status = fields.String()
    student_id = fields.Integer()
    tutor_id = fields.Integer()
    course_id = fields.Integer()
get_tutorships_count_input_schema = GetTutorshipsCountInputSchema()
@app.route('/api/tutorships/count/', methods=['GET'])
@requires_auth
def get_tutorship_count():
    errors = get_tutorships_count_input_schema.validate(request.args)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400
    
    try:
        id = request.args.get('id')
        status = request.args.get('status')
        student_id = request.args.get('student_id')
        tutor_id = request.args.get('tutor_id')
        course_id = request.args.get('course_id')

        filters = []
        if id:
            filters.append(Tutorships.id == id)
        if status:
            filters.append(Tutorships.status == status)
        if student_id:
            filters.append(Tutorships.student_id == student_id)
        if tutor_id:
            filters.append(Tutorships.tutor_id == tutor_id)
        if course_id:
            filters.append(Tutorships.course_id == course_id)

        tutorship_count = Tutorships.query.filter(*filters).count()
        return jsonify({"count": tutorship_count})
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400




""" POST /api/tutorship/create
Parameters:
    - status        (str)!
    - student_id    (int)!
    - tutor_id      (int)!
    - course_id      (int)!
"""
class CreateTutorshipsInputSchema(Schema):
    status = fields.String(required=True)
    student_id = fields.Integer(required=True)
    tutor_id = fields.Integer(required=True)
    course_id = fields.Integer(required=True)
create_tutorships_input_schema = CreateTutorshipsInputSchema()

@app.route('/api/tutorship/create/', methods=['POST'])
@requires_auth
def create_tutorship():
    data = json.loads(request.data)
    errors = create_tutorships_input_schema.validate(data)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400
    
    try:
        status = data.get('status')
        student_id = data.get('student_id')
        tutor_id = data.get('tutor_id')
        course_id = data.get('course_id')

        # check that student_id is a student
        filters = []
        filters.append(Users.id == student_id)
        filters.append(Users.is_student == True)
        student = Users.query.filter(*filters).first()
        if student is None:
            return {"message": "Given student id must be a student."}, 400

        filters = []
        filters.append(Users.id == tutor_id)
        filters.append(Users.is_tutor == True)
        tutor = Users.query.filter(*filters).first()
        if tutor is None:
            return {"message": "Given tutor id must be a tutor."}, 400

        
        filters = []
        filters.append(Courses.id == course_id)
        course = Courses.query.filter(*filters).first()
        if course is None:
            return {"message": "Given course must exist."}, 400

        # check that tutor_course has been approved
        filters = []
        filters.append(TutorCourses.tutor_id == tutor_id)
        filters.append(TutorCourses.course_id == course_id)
        filters.append(TutorCourses.status == 'ACCEPTED')
        tutor_course = TutorCourses.query.filter(*filters).first()
        if tutor_course is None:
            return {"message": "Given tutor must have an accepted status with the given course."}, 400

        # Prevent duplicate tutorships (where student, tutor, and course repeat)
        filters = []
        filters.append(Tutorships.student_id == student_id)
        filters.append(Tutorships.tutor_id == tutor_id)
        filters.append(Tutorships.course_id == course_id)
        duplicate_tutorship = Tutorships.query.filter(*filters).first()
        if duplicate_tutorship is not None:
            return {"message": "Cannot create duplicate tutorships."}, 400

        # create tutorship in database
        tutorship = Tutorships(status, student_id, tutor_id, course_id)
        db.session.add(tutorship)
        db.session.commit()

        # send email notification
        tutor = tutor.serialize()
        student = student.serialize()
        course = course.serialize()
        if data.get('status') not in [None, '']:
            try:
                if data.get('status') == 'REQUESTED':
                    send_tutorship_request_email(tutor['email'], student['name'], course['name'])
                elif data.get('status') == 'ACCEPTED':
                    send_tutorship_accept_email(student['email'], tutor['name'], course['name'])
                elif data.get('status') == 'REJECTED':
                    send_tutorship_deny_email(student['email'], tutor['name'], course['name'])
            except Exception as e:
                print("email sending failed: " + str(e))

        return {"message": "success" }, 200
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400





""" POST /api/tutorship/update
Parameters:
    - id            (int)!
    - status        (str)?
    - student_id    (int)?
    - tutor_id      (int)?
    - course_id      (int)?
"""
class UpdateTutorshipsInputSchema(Schema):
    id = fields.Integer(required=True)
    status = fields.String()
    student_id = fields.Integer()
    tutor_id = fields.Integer()
    course_id = fields.Integer()
update_tutorships_input_schema = UpdateTutorshipsInputSchema()

@app.route('/api/tutorship/update', methods=['POST'])
@requires_auth
def  update_tutorship():
    data = json.loads(request.data)
    errors = update_tutorships_input_schema.validate(data)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400
    
    try:
        id = data.get('id')

        tutorship = Tutorships.query.filter(Tutorships.id == id).first()
        if tutorship is None:
            return {"message": "Tutorship could not be found."}, 400
        
        if data.get('status') not in [None, '']:
            tutorship.status = data.get('status')

            # check that tutor_course has been approved
            filters = []
            filters.append(TutorCourses.tutor_id == tutorship.tutor_id)
            filters.append(TutorCourses.course_id == tutorship.course_id)
            filters.append(TutorCourses.status == 'ACCEPTED')
            tutor_course = TutorCourses.query.filter(*filters).first()
            if tutor_course is None:
                return {"message": "Given tutor must have an accepted status with the given course."}, 400


        if data.get('student_id') not in [None, '']:
            tutorship.student_id = data.get('student_id')
        if data.get('tutor_id') not in [None, '']:
            tutorship.tutor_id = data.get('tutor_id')
        if data.get('course_id') not in [None, '']:
            tutorship.course_id = data.get('course_id')

        db.session.commit()

        
        # get student
        filters = []
        filters.append(Users.id == tutorship.student_id)
        filters.append(Users.is_student == True)
        student = Users.query.filter(*filters).first()
        if student is None:
            return {"message": "Given student id must be a student."}, 400
        student = student.serialize()

        # get tutor
        filters = []
        filters.append(Users.id == tutorship.tutor_id)
        filters.append(Users.is_tutor == True)
        tutor = Users.query.filter(*filters).first()
        if tutor is None:
            return {"message": "Given tutor id must be a tutor."}, 400
        tutor = tutor.serialize()

        # get course
        filters = []
        filters.append(Courses.id == tutorship.course_id)
        course = Courses.query.filter(*filters).first()
        if course is None:
            return {"message": "Given course must exist."}, 400
        course = course.serialize()

         # send email notification
        if data.get('status') not in [None, '']:
            try:
                if data.get('status') == 'REQUESTED':
                    send_tutorship_request_email(tutor['email'], student['name'], course['name'])
                elif data.get('status') == 'ACCEPTED':
                    send_tutorship_accept_email(student['email'], tutor['name'], course['name'])
                elif data.get('status') == 'REJECTED':
                    send_tutorship_deny_email(student['email'], tutor['name'], course['name'])
            except Exception as e:
                print("email sending failed: " + str(e))


        return {"message": "success" }, 200
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400





""" POST /api/tutorship/delete
Parameters:
    - id (int)!
"""
class DeleteTutorshipInputSchema(Schema):
    id = fields.Integer(required=True)
delete_tutorship_input_schema = DeleteTutorshipInputSchema()

@app.route('/api/tutorship/delete/', methods=['POST'])
@requires_auth
def delete_tutorship():
    data = json.loads(request.data)
    errors = delete_tutorship_input_schema.validate(data)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400

    try:
        id = data.get('id')
        tutorship = Tutorships.query.filter(Tutorships.id == id).first()
        if tutorship is None:
            return {"message": "Tutorship could not be found."}, 400

        db.session.delete(tutorship)
        db.session.commit()
        return {"message": "success"}
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400

