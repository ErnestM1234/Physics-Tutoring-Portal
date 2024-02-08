import json
from app import app, db, context
from flask import jsonify, request
from marshmallow import Schema, fields
from src.utils.auth import requires_auth
from src.database.models import TutorCourses, Users, Courses, Tutorships
from src.services.gmail_service.gmail_service import send_tutor_course_first_accept_email, send_tutor_course_accept_email, send_tutor_course_deny_email


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
            # get sub objects
            tutor = Users.query.filter(Users.id == tutor_course["tutor_id"]).first()
            if tutor:
                tutor_course["tutor"] = tutor.serialize()
            course = Courses.query.filter(Courses.id == tutor_course["course_id"]).first()
            if course:
                tutor_course["course"] = course.serialize()
            # get counts
            tutor_course["tutor_total_accepted_tutorship_count"] = 0
            tutor_course["accepted_tutorship_count"] = 0
            
            count = Tutorships.query.filter(*[
                Tutorships.status == "ACCEPTED",
                Tutorships.tutor_id == tutor_course["tutor_id"],
            ]).count()
            if count:
                tutor_course["tutor_total_accepted_tutorship_count"] = count
            count = Tutorships.query.filter(*[
                Tutorships.status == "ACCEPTED",
                Tutorships.tutor_id == tutor_course["tutor_id"],
                Tutorships.course_id == tutor_course["course_id"]
            ]).count()
            if count:
                tutor_course["accepted_tutorship_count"] = count

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

        # check that tutor_id is a tutor
        filters = []
        filters.append(Users.id == tutor_id)
        filters.append(Users.is_tutor == True)
        tutor = Users.query.filter(*filters).first()
        if tutor is None:
            return {"message": "Given user must be a tutor to have an accepted status for a tutor_course relationship."}, 400

        # Prevent duplicate tutor_courses (where tutor and course repeat)
        filters = []
        filters.append(TutorCourses.tutor_id == tutor_id)
        filters.append(TutorCourses.course_id == course_id)
        duplicate_tutor_course = TutorCourses.query.filter(*filters).first()
        if duplicate_tutor_course is not None:
            return {"message": "Cannot create duplicate tutor_courses."}, 400
        
        # create tutor course
        tutor_course = TutorCourses(tutor_id, course_id, status, taken_course, experience)
        db.session.add(tutor_course)
        db.session.commit()

        # send update email
        if data.get('status') not in [None, '']:
            try:
                # get course
                filters = []
                filters.append(Courses.id == course_id)
                course = Courses.query.filter(*filters).first()
                if course is None:
                    raise Exception("course could not be found")
                course = course.serialize()

                # get tutor
                tutor = tutor.serialize()

                # send message
                if data.get('status') == 'ACCEPTED':
                    # check if this is the first course the tutor is tutoring
                    filters = []
                    filters.append(TutorCourses.tutor_id == tutor_id)
                    filters.append(TutorCourses.status in ['ACCEPTED', 'UNAVAILABLE'])
                    if TutorCourses.query.filter(*filters).count() <= 1:
                        # send first tutor_course email
                        send_tutor_course_first_accept_email(tutor["email"], tutor["name"], course["name"])
                    else:
                        # send generic tutor_course email
                        send_tutor_course_accept_email(tutor["email"], course["name"])
                elif data.get('status') == 'DENIED':
                    send_tutor_course_deny_email(tutor["email"], course["name"])

            except Exception as e:
                print("email sending failed: " + str(e))

        
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
@requires_auth
def  update_tutor_course():
    data = json.loads(request.data)
    errors = update_tutor_course_input_schema.validate(data)
    if errors:
        print(str(errors))
        return {"message": str(errors) }, 400

    try:
        # get tutor_course
        id = data.get('id')
        tutor_course = TutorCourses.query.filter(TutorCourses.id == id).first()
        if tutor_course is None:
            return {"message": "Tutor course could not be found."}, 400
        
        # get access_level
        user = context['user']
        if user is None:
            return {"message": "User could not be found."}, 400
        access_level = None
        if user.is_admin: access_level = "ADMIN"
        elif user.is_tutor: access_level = "TUTOR"
        elif user.is_student: access_level = "STUDENT"

        # get tutor_id
        tutor_id = data.get('tutor_id', None)
        if tutor_id == None:
            tutor_id = tutor_course.tutor_id
        
        # Tutor Updates:
        # TODO: In the case that the person updating is an admin, check if the admin is the tutor in question. In this case, no need for
        # sending email updating them if they have been accepted into the course
        if user.id == tutor_id and access_level == "TUTOR":
            # Tutors can only update their statuses as follows:
            # ---Beginning Status--- ---Updated Status---

            # - DENIED             ->   DENIED
            # - DENIED             ->   REQUESTED

            # - UNAVAILBLE         ->   UNAVAILBLE
            # - UNAVAILBLE         ->   ACCEPTED    (which here means available for teaching)

            # - REQUESTED          ->   REQUESTED

            # - ACCEPTED           ->   ACCEPTED
            # - ACCEPTED           ->   UNAVAILABLE

            # get new status
            cur_status = tutor_course.status
            new_status = data.get('status', None)

            # state machine logic
            if cur_status == "DENIED": # state = DENIED
                if new_status == "DENIED" or new_status == "REQUESTED":
                    # update the status
                    tutor_course.status = new_status
                    db.session.commit()
                    return {"message": "success"}, 200
                else:
                    # return an error
                    print("Tutor is unauthorized to perform this action.")
                    return {"error": str("Tutor is unauthorized to perform this action.")}, 401
                
            elif cur_status == "UNAVAILABLE": # state = UNAVAILABLE
                if new_status == "UNAVAILABLE" or new_status == "ACCEPTED":
                    # update the status
                    tutor_course.status = new_status
                    db.session.commit()
                    return {"message": "success"}, 200
                else:
                    # return an error
                    print("Tutor is unauthorized to perform this action.")
                    return {"error": str("Tutor is unauthorized to perform this action.")}, 401
                
            elif cur_status == "REQUESTED": # state = REQUESTED
                if new_status == "REQUESTED":
                    # update the status
                    tutor_course.status = new_status
                    db.session.commit()
                    return {"message": "success"}, 200
                else:
                    # return an error
                    print("Tutor is unauthorized to perform this action.")
                    return {"error": str("Tutor is unauthorized to perform this action.")}, 401
                
            elif cur_status == "ACCEPTED": # state = ACCEPTED
                if new_status == "ACCEPTED" or new_status == "UNAVAILABLE":
                    # update the status
                    tutor_course.status = new_status
                    db.session.commit()
                    return {"message": "success"}, 200
                else:
                    # return an error
                    print("Tutor is unauthorized to perform this action.")
                    return {"error": str("Tutor is unauthorized to perform this action.")}, 401

            else: # state = ???
                # return an error
                print("Tutor is unauthorized to perform this action.")
                return {"error": str("Tutor is unauthorized to perform this action.")}, 401

        # Admin Updates:
        elif access_level == "ADMIN":
            # get tutor_id and course_id (for sending email later)
            ser_tutor_course = tutor_course.serialize()
            tutor_id = ser_tutor_course["tutor_id"]
            course_id = ser_tutor_course["course_id"]
            tutor = None

            # update tutor_course relationship
            if data.get('tutor_id') not in [None, '']:
                # check that tutor_id is a tutor (if they are updating tutor_id)
                filters = []
                filters.append(Users.id == data.get('tutor_id'))
                filters.append(Users.is_tutor == True)
                tutor = Users.query.filter(*filters).first()
                if tutor is None:
                    return {"message": "Given user must be a tutor to have an accepted status for a tutor_course relationship."}, 400
                # update tutor_course object
                tutor_course.tutor_id = data.get('tutor_id')
                # set tutor_id to the new tutor_id
                tutor_id = data.get('tutor_id')
            if data.get('course_id') not in [None, '']:
                tutor_course.course_id = data.get('course_id')
                course_id = data.get('course_id')
            if data.get('status') not in [None, '']:
                tutor_course.status = data.get('status')
            if data.get('taken_course') not in [None, '']:
                tutor_course.taken_course = data.get('taken_course')
            if data.get('experience') not in [None, '']:
                tutor_course.experience = data.get('experience')

            db.session.commit()

            # send update email
            if data.get('status') not in [None, '']:
                try:
                    # get course
                    filters = []
                    filters.append(Courses.id == course_id)
                    course = Courses.query.filter(*filters).first()
                    if course is None:
                        raise Exception("course could not be found")
                    course = course.serialize()

                    # get tutor
                    if not tutor: # check if got tutor from earlier
                        filters = []
                        filters.append(Users.id == tutor_id)
                        filters.append(Users.is_tutor == True)
                        tutor = Users.query.filter(*filters).first()
                        if tutor is None:
                            raise Exception("tutor could not be found")
                    tutor = tutor.serialize()

                    # send email message
                    if data.get('status') == 'ACCEPTED' or data.get('status') == 'UNAVAILABLE':
                        # check if this is the first course the tutor is tutoring
                        filters = []
                        filters.append(TutorCourses.tutor_id == tutor_id)
                        filters.append(TutorCourses.status == 'ACCEPTED' or TutorCourses.status == 'UNAVAILABLE')
                        if TutorCourses.query.filter(*filters).count() <= 1:
                            # send first tutor_course email
                            send_tutor_course_first_accept_email(tutor["email"], tutor["name"], course["name"])
                        else:
                            # send generic tutor_course email
                            send_tutor_course_accept_email(tutor["email"], course["name"])
                    elif data.get('status') == 'DENIED':
                        send_tutor_course_deny_email(tutor["email"], course["name"])

                except Exception as e:
                    print("email sending failed: " + str(e))
            return {"message": "success"}, 200
        else: # student
            print("Unauthorized")
            return {"error": str("Unauthorized")}, 401

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
