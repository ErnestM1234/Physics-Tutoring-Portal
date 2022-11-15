from app import app, db
from flask import jsonify, request
from marshmallow import Schema, fields
from src.database.models import TutorCourses


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
        return {"message": str(errors) }, 400
    
    try:
        id = request.args.get('id')
        tutor_course = TutorCourses.query.filter(TutorCourses.id == id).first()
        if tutor_course is None:
            return {"message": "Tutor course could not be found."}, 400
        return jsonify(tutor_course.serialize())
    except Exception as e:
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
get_tutor_courses_input_schema = GetTutorCoursesInputSchema()

@app.route('/api/tutor_courses/', methods=['GET']) 
def get_tutor_courses():
    errors = get_tutor_courses_input_schema.validate(request.args)
    if errors:
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

        tutor_courses = TutorCourses.query.filter(*filters).all()
        return jsonify([tutor_course.serialize() for tutor_course in tutor_courses ])
   
    except Exception as e:
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

@app.route('/api/tutor_course/create', methods=['POST'])
def create_tutor_course():
    errors = create_tutor_course_input_schema.validate(request.form)
    if errors:
        return {"message": str(errors) }, 400
    
    try:
        tutor_course = TutorCourses(request.form['tutor_id'], request.form['course_id'], request.form['status'])
        db.session.add(tutor_course)
        db.session.commit()
        return {"message": "success" }, 200
    except Exception as e:
        return {"error": str(e)}, 400




""" POST /api/user/update
Parameters:
    - id          (int)!
    - name        (string)?
    - netid       (string)?
    - email       (string)?
    - bio         (string)?
    - is_student  (boolean)?
    - is_tutor    (boolean)?
    - is_admin    (boolean)?
"""
class UpdateUserInputSchema(Schema):
    id = fields.String(required=True)
    netid = fields.String()
    name = fields.String()
    email = fields.String()
    bio = fields.String()
    is_student = fields.Boolean()
    is_tutor = fields.Boolean()
    is_admin = fields.Boolean()
update_user_input_schema = UpdateUserInputSchema()

@app.route('/api/tutor_course/update', methods=['POST'])
def  update_tutor_course():
    return 'update tutor_course'



@app.route('/api/tutor_course/delete', methods=['POST'])
def delete_tutor_course():
    return 'delete tutor_course'
