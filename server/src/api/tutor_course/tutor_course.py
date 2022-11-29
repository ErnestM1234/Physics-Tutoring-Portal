import json
from app import app, db
from flask import jsonify, request
from marshmallow import Schema, fields
from src.database.models import TutorCourses, Courses, Users


""" GET /api/tutor_course/
Parameters:
    - id (int)!
"""
class GetTutorCourseInputSchema(Schema):
    id = fields.Integer(required=True)
get_tutor_course_input_schema = GetTutorCourseInputSchema()

@app.route('/api/tutor_course/', methods=['GET'])
def get_tutor_course():
    errors = get_tutor_course_input_schema.validate(request.args)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400
    
    try:
        id = request.args.get('id')
        tutor_course = TutorCourses.query.filter(TutorCourses.id == id).first()
        if tutor_course is None:
            return {"message": "Tutor course could not be found."}, 400
        return jsonify(tutor_course.serialize())
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400




""" GET /api/tutor_courses/
Parameters:
    - tutor_id (int)?
    - course_id (int)?
    - status (string)?
"""
class GetTutorCoursesInputSchema(Schema):
    tutor_id = fields.Integer()
    course_id = fields.Integer()
    status = fields.String()
    tutor = fields.Boolean()
    course = fields.Boolean()
get_tutor_courses_input_schema = GetTutorCoursesInputSchema()

@app.route('/api/tutor_courses/', methods=['GET']) 
def get_tutor_courses():
    errors = get_tutor_courses_input_schema.validate(request.args)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400

    try:
        tutor_id = request.args.get('tutor_id')
        course_id = request.args.get('course_id')
        status = request.args.get('status')
        tutor = request.args.get('tutor')
        course = request.args.get('course')

        filters = []
        if tutor_id:
            filters.append(TutorCourses.tutor_id == tutor_id)
        if course_id:
            filters.append(TutorCourses.course_id == course_id)
        if status:
            filters.append(TutorCourses.status == status)

        tutor_courses = TutorCourses.query.filter(*filters).all()
        serialized_tutorships = [tutorship.serialize() for tutor_courses in tutor_courses]
        for tutorship in serialized_tutorships:
            if tutor:
                tutorship['tutor'] = Users.query.filter(Users.id == tutorship['tutor_id']).first().serialize()
            if course:
                tutorship['course'] = Courses.query.filter(Courses.id == tutorship['course_id']).first().serialize()
        return jsonify(serialized_tutorships)
   
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400


""" GET /api/tutor_course/tutor_count/
Parameters:
    - tutor_id (int)?
    - course_id (int)?
    - status (string)?
"""
class GetTutorCourseCountInputSchema(Schema):
    tutor_id = fields.Integer()
    course_id = fields.Integer()
    status = fields.String()
get_tutor_courses_count_input_schema = GetTutorCourseCountInputSchema()

@app.route('/api/tutor_course/count/', methods=['GET']) 
def get_tutor_course_tutor_count():
    errors = get_tutor_courses_count_input_schema.validate(request.args)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400

    try:
        tutor_id = request.args.get('tutor_id')
        course_id = request.args.get('course_id')
        status = request.args.get('status')

        filters = []
        if tutor_id:
            filters.append(TutorCourses.tutor_id == tutor_id)
        if course_id:
            filters.append(TutorCourses.course_id == course_id)
        if status:
            filters.append(TutorCourses.status == status)

        count = TutorCourses.query.filter(*filters).count()
        return jsonify(count)
   
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400

             

""" POST /api/tutor_course/create/
Parameters:
    - tutor_id  (int)!
    - course_id  (int)!
    - status    (string)!
"""
class CreateTutorCourseInputSchema(Schema):
    tutor_id = fields.Integer(required=True)
    course_id = fields.Integer(required=True)
    status = fields.String(required=True)
create_tutor_course_input_schema = CreateTutorCourseInputSchema()

@app.route('/api/tutor_course/create/', methods=['POST'])
def create_tutor_course():
    data = json.loads(request.data)
    errors = create_tutor_course_input_schema.validate(data)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400
    
    try:
        tutor_course = TutorCourses(data.get('tutor_id'), data.get('course_id'), data.get('status'))
        db.session.add(tutor_course)
        db.session.commit()
        return {"message": "success" }, 200
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400




""" POST /api/tutor_course/update
Parameters:
    - id        (int)!
    - tutor_id  (int)?
    - course_id (int)?
    - status    (string)?
"""
class UpdateTutorCourseInputSchema(Schema):
    id = fields.Integer(required=True)
    tutor_id = fields.Integer()
    course_id = fields.Integer()
    status = fields.String()
update_tutor_course_input_schema = UpdateTutorCourseInputSchema()

@app.route('/api/tutor_course/update/', methods=['POST'])
def  update_tutor_course():
    data = json.loads(request.data)
    errors = update_tutor_course_input_schema.validate(data)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400

    try:
        id = data.get('id')
        tutor_course = TutorCourses.query.filter(TutorCourses.id == id).first()
        if tutor_course is None:
            return {"message": "Tutor course could not be found."}, 400
        # todo (Ernest): find if there is a better way to do this
        if data.get('tutor_id') not in [None, '']:
            tutor_course.tutor_id = data.get('tutor_id')
        if data.get('course_id') not in [None, '']:
            tutor_course.course_id = data.get('course_id')
        if data.get('status') not in [None, '']:
            tutor_course.status = data.get('status')
        db.session.commit()
        return {"message": "success" }, 200
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400


""" POST /api/tutor_course/delete
Parameters:
    - id (int)!
"""
class DeleteTutorCourseInputSchema(Schema):
    id = fields.Integer(required=True)
delete_tutor_course_input_schema = DeleteTutorCourseInputSchema()

@app.route('/api/tutor_course/delete/', methods=['POST'])
def delete_tutor_course():
    data = json.loads(request.data)
    errors = delete_tutor_course_input_schema.validate(data)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400

    try:
        id = data.get('id')
        tutor_course = TutorCourses.query.filter(TutorCourses.id == id).first()
        if tutor_course is None:
            tutor_course = {"message": "Tutor course could not be found."}, 400
        db.session.delete(tutor_course)
        db.session.commit()
        return {"message": "success" }, 200
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400
