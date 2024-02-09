from app import app, context
from flask import jsonify
from src.database.models import Courses, TutorCourses, Tutorships, Users
from src.utils.auth import requires_auth


""" GET /api/dashboard_stats/
Parameters:
    - None
"""
@app.route('/api/dashboard_stats/', methods=['GET'])
@requires_auth
def get_dashboard_stats():
    try:
        # get user
        user = context['user']
        if user is None:
            return {"message": "User could not be found."}, 400
        
        # enforce authorization level is admin
        if not user.is_admin:
            print(str("This is an unauthorized action"))
            return {"error": str("This is an unauthorized action")}, 401
        
        # get course stats
        courses = [course.serialize() for course in Courses.query.all()]
        accepted_tutorships = [tutorship.serialize() for tutorship in Tutorships.query.filter(Tutorships.status == "ACCEPTED").all()]
        approved_tutor_courses = [tutor_course.serialize() for tutor_course in TutorCourses.query.filter((TutorCourses.status == "ACCEPTED") | (TutorCourses.status == "UNAVAILABLE")).all()]
        if courses is None or accepted_tutorships is None or approved_tutor_courses is None:
            print("Failed to fetch statistics")
            return {"message": "Failed to fetch statistics"}, 400
        # count tutees and approved tutors by course
        tutee_counts = {}
        for tutorship in accepted_tutorships:
            tutee_counts[str(tutorship["course_id"])] = 1 + tutee_counts.get(str(tutorship["course_id"]), 0)
        acceted_tutor_counts = {}
        for tutor_course in approved_tutor_courses:
            acceted_tutor_counts[str(tutor_course["course_id"])] = 1 + acceted_tutor_counts.get(str(tutor_course["course_id"]), 0)
        # add counts to courses
        for course in courses:
            course["tutees_count"] = tutee_counts.get(str(course["id"]), 0)
            course["approved_tutors_count"] = acceted_tutor_counts.get(str(course["id"]), 0)

        # get aggregated stats
        course_count = len(courses)
        student_count = Users.query.filter(Users.is_student == True).count()
        approved_tutor_count = len(set([tutor_course["tutor_id"] for tutor_course in approved_tutor_courses]))
        stats = {
            "course_count": course_count,
            "student_count": student_count,
            "tutor_approved_count": approved_tutor_count,
            "courses": courses
        }
        return jsonify(stats) 

    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 400
