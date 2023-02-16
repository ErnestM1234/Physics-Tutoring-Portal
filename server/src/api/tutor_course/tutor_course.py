import json
from app import app, db
from flask import jsonify, request
from marshmallow import Schema, fields
from src.database.models import TutorCourses, Users, Courses


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
        print(str(e))
        return {"error": str(e)}, 400


""" GET /api/tutor_courses/deep/
Parameters:
    - tutor_id (int)?
    - course_id (int)?
    - status (string)?
"""
class GetTutorCoursesDeepInputSchema(Schema):
    tutor_id = fields.Integer()
    course_id = fields.Integer()
    status = fields.String()
get_tutor_courses_deep_input_schema = GetTutorCoursesDeepInputSchema()

@app.route('/api/tutor_courses/deep/', methods=['GET']) 
def get_tutor_courses_deep():
    errors = get_tutor_courses_deep_input_schema.validate(request.args)
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

        result = TutorCourses.query.filter(*filters).all()
        tutor_courses = [tutor_course.serialize() for tutor_course in result]
        # get courses and tutors
        for tutor_course in tutor_courses:
            # get user
            try:
                user = Users.query.filter(Users.id == tutor_course['tutor_id']).first()
                if user is not None:
                    tutor_course['tutor'] = user.serialize()
            except Exception as e:
                print("Failed to query user for /api/tutor_courses/deep/")
                print("Exception:" + e)

            # get course
            try:
                course = Courses.query.filter(Courses.id == tutor_course['course_id']).first()
                if course is not None:
                        tutor_course['course'] = course.serialize()
            except Exception as e:
                print("Failed to query course for /api/tutor_courses/deep/")
                print("Exception:" + e)

        return jsonify(tutor_courses)
   
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400


             

""" POST /api/tutor_course/create/
Parameters:
    - tutor_id      (int)!
    - course_id     (int)!
    - status        (string)!
    - taken_course  (string)?
    - experience    (string)?
"""
class CreateTutorCourseInputSchema(Schema):
    tutor_id = fields.Integer(required=True)
    course_id = fields.Integer(required=True)
    status = fields.String(required=True)
    taken_course = fields.String()
    experience = fields.String()
create_tutor_course_input_schema = CreateTutorCourseInputSchema()

@app.route('/api/tutor_course/create/', methods=['POST'])
def create_tutor_course():
    data = json.loads(request.data)
    errors = create_tutor_course_input_schema.validate(data)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400
    
    try:
        tutor_id = data.get('tutor_id')
        course_id = data.get('course_id')
        status = data.get('status')
        taken_course = data.get('taken_course') or ''
        experience = data.get('experience') or ''

        # only approved tutors can have an accepted status
        if status == "ACCEPTED":
            # check that tutor_id is a tutor
            filters = []
            filters.append(Users.id == tutor_id)
            filters.append(Users.is_tutor == True)
            tutor = Users.query.filter(*filters).first()
            if tutor is None:
                return {"message": "Given user must be a tutor to have an accepted status for tutoring a course."}, 400

        # Prevent duplicate tutor_courses (where tutor and course repeat)
        filters = []
        filters.append(TutorCourses.tutor_id == tutor_id)
        filters.append(TutorCourses.course_id == course_id)

        duplicate_tutor_course = TutorCourses.query.filter(*filters).first()

        if duplicate_tutor_course is None:
            tutor_course = TutorCourses(tutor_id, course_id, status, taken_course, experience)
            db.session.add(tutor_course)
            db.session.commit()
            return {"message": "success" }, 200
        else:
            return {"message": "Cannot create duplicate tutor_courses."}, 400
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400




""" POST /api/tutor_course/update
Parameters:
    - id        (int)!
    - tutor_id  (int)?
    - course_id (int)?
    - status    (string)?
    - taken_course  (string)?
    - experience    (string)?
"""
class UpdateTutorCourseInputSchema(Schema):
    id = fields.Integer(required=True)
    tutor_id = fields.Integer()
    course_id = fields.Integer()
    status = fields.String()
    taken_course = fields.String()
    experience = fields.String()
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


        if data.get('tutor_id') not in [None, '']:
            tutor_course.tutor_id = data.get('tutor_id')
        if data.get('course_id') not in [None, '']:
            tutor_course.course_id = data.get('course_id')
        if data.get('status') not in [None, '']:
            tutor_course.status = data.get('status')
        if data.get('taken_course') not in [None, '']:
            tutor_course.taken_course = data.get('taken_course')
        if data.get('experience') not in [None, '']:
            tutor_course.experience = data.get('experience')

            # only approved tutors can have an accepted status
            if tutor_course.status == "ACCEPTED":
                # check that tutor_id is a tutor
                filters = []
                filters.append(Users.id == tutor_course.tutor_id)
                filters.append(Users.is_tutor == True)
                tutor = Users.query.filter(*filters).first()
                if tutor is None:
                    return {"message": "Given user must be a tutor to have an accepted status for tutoring a course."}, 400

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
