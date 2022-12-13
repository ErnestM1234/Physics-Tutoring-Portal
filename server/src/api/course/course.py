import json
from app import app, db
from flask import jsonify, request
from src.database.models import Courses
from marshmallow import Schema, fields
from src.utils.auth import requires_auth


""" GET /api/course/
Parameters:
    - id (int)!
"""
class GetCourseInputSchema(Schema):
    id = fields.Integer(required=True)
get_course_input_schema = GetCourseInputSchema()

@app.route('/api/course/', methods=['GET'])
@requires_auth
def read_course():
    errors = get_course_input_schema.validate(request.args)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400
    
    try:
        id = request.args.get('id')
        course = Courses.query.filter(Courses.id == id).first()
        if course is None:
            return {"message": "Course could not be found."}, 400
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400

    return jsonify(course.serialize())





""" GET /api/courses/
Parameters:
    - id            (int)?
    - name          (str)?
    - dept_course   (str)?
"""
class GetCoursesInputSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    dept_course = fields.String()
get_courses_input_schema = GetCoursesInputSchema()

@app.route('/api/courses/', methods=['GET'])
@requires_auth
def get_courses():
    errors = get_courses_input_schema.validate(request.args)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400

    try:
        id = request.args.get('id')
        name = request.args.get('name')
        dept_course = request.args.get('dept_course')

        filter = []
        if id:
            filter.append(Courses.id == id)
        if name:
            filter.append(Courses.name == name)
        if dept_course:
            filter.append(Courses.dept_course == dept_course)
        courses = Courses.query.filter(*filter).all()
        return jsonify([course.serialize() for course in courses])
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400





""" POST /api/course/create
Parameters:
    - name          (str)!
    - dept_course   (str)!
"""
class CreateCourseInputSchema(Schema):
    name = fields.String(required=True)
    dept_course = fields.String(required=True)
create_course_input_schema = CreateCourseInputSchema()

@app.route('/api/course/create/', methods=['POST'])
@requires_auth
def create_course():
    data = json.loads(request.data)
    errors = create_course_input_schema.validate(data)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400
    
    try:
        course = Courses.query.filter(Courses.name == data.get('name')).first()
        if course is not None:
            return {"message": "Failed to create course. A course with this name already exists." }, 400

        course = Courses(data.get('name'), data.get('dept_course'))
        db.session.add(course)
        db.session.commit()
        return {"message": "success" }, 200
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400




""" POST /api/course/update
Parameters:
    - id            (int)!
    - name          (str)?
    - dept_course   (str)?
"""
class UpdateCourseInputSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String()
    dept_course = fields.String()
update_course_input_schema = UpdateCourseInputSchema()

@app.route('/api/course/update', methods=['POST'])
@requires_auth
def  update_course():
    data = json.loads(request.data)
    errors = update_course_input_schema.validate(data)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400
    
    try:
        id = data.get('id')
        course = Courses.query.filter(Courses.id == id).first()
        if course is None:
            return {"message": "Course could not be found."}, 400
        
        if data.get('name') not in [None, '']:
            course.name = data.get('name')
        if data.get('dept_course') not in [None, '']:
            course.dept_course = data.get('dept_course')
        db.session.add(course)
        db.session.commit()
        return {"message": "success" }, 200
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400





""" POST /api/course/
Parameters:
    - id (int)!
"""
class DeleteCourseInputSchema(Schema):
    id = fields.Integer(required=True)
delete_course_input_schema = DeleteCourseInputSchema()

@app.route('/api/course/delete/', methods=['POST'])
@requires_auth
def delete_course():
    data = json.loads(request.data)
    errors = delete_course_input_schema.validate(data)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400

    try:
        id = data.get('id')
        course = Courses.query.filter(Courses.id == id).first()
        if course is None:
            return {"message": "Course could not be found."}, 400
        db.session.delete(course)
        db.session.commit()
        return {"message": "success" }, 200
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400
