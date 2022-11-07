from app import app, db
from flask import jsonify, request
from src.database.models import Courses
from marshmallow import Schema, fields


""" GET /api/course/
Parameters:
    - id (int)!
"""
class GetCourseInputSchema(Schema):
    id = fields.Integer(required=True)
get_course_input_schema = GetCourseInputSchema()

@app.route('/api/course/', methods=['GET'])
def read_course():
    errors = get_course_input_schema.validate(request.args)
    if errors:
        return {"message": str(errors) }, 400
    
    try:
        id = request.args['id']
        course = Courses.query.filter(Courses.id == id).first()
        if course is None:
            return {"message": "Course could not be found."}, 400
    except Exception as e:
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
def get_courses():
    errors = get_courses_input_schema.validate(request.args)
    if errors:
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

@app.route('/api/course/create', methods=['POST'])
def create_course():
    errors = create_course_input_schema.validate(request.form)
    if errors:
        return {"message": str(errors) }, 400
    
    try:
        course = Courses(request.form['name'], request.form['dept_course'])
        db.session.add(course)
        db.session.commit()
        return {"message": "success" }, 200
    except Exception as e:
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
def  update_course():
    errors = update_course_input_schema.validate(request.form)
    if errors:
        return {"message": str(errors) }, 400
    
    try:
        id = request.form['id']
        course = Courses.query.filter(Courses.id == id).first()
        if course is None:
            return {"message": "Course could not be found."}, 400
        
        if request.form['name'] not in [None, '']:
            course.name = request.form['name']
        if request.form['dept_course'] not in [None, '']:
            course.dept_course = request.form['dept_course']
        db.session.add(course)
        db.session.commit()
        return {"message": "success" }, 200
    except Exception as e:
        return {"error": str(e)}, 400





""" POST /api/course/
Parameters:
    - id (int)!
"""
class DeleteCourseInputSchema(Schema):
    id = fields.Integer(required=True)
delete_course_input_schema = DeleteCourseInputSchema()

@app.route('/api/course/delete', methods=['POST'])
def delete_course():
    errors = delete_course_input_schema.validate(request.form)
    if errors:
        return {"message": str(errors) }, 400

    try:
        id = request.form['id']
        course = Courses.query.filter(Courses.id == id).first()
        if course is None:
            return {"message": "Course could not be found."}, 400
        db.session.delete(course)
        db.session.commit()
        return {"message": "success" }, 200
    except Exception as e:
        return {"error": str(e)}, 400
