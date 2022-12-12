import json
from app import app, db
from flask import jsonify, request
from src.utils.auth import requires_auth
from src.database.models import Tutorships, TutorCourses, Users
from marshmallow import Schema, fields


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
            return {"message": "Given student id must be a student have a tutorship."}, 400

        # check that tutor_id is a tutor
        filters = []
        filters.append(Users.id == tutor_id)
        filters.append(Users.is_tutor == True)
        tutor = Users.query.filter(*filters).first()
        if tutor is None:
            return {"message": "Given tutor id must be a tutor have a tutorship."}, 400

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

        if duplicate_tutorship is None:
            tutorship = Tutorships(status, student_id, tutor_id, course_id)
            db.session.add(tutorship)
            db.session.commit()
            return {"message": "success" }, 200
        else:
            return {"message": "Cannot create duplicate tutorships."}, 400
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
        if data.get('student_id') not in [None, '']:
            tutorship.student_id = data.get('student_id')
        if data.get('tutor_id') not in [None, '']:
            tutorship.tutor_id = data.get('tutor_id')
        if data.get('course_id') not in [None, '']:
            tutorship.course_id = data.get('course_id')

        db.session.commit()
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

