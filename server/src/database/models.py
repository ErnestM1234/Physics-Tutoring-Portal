# this is a file containing our datamodels
from app import db

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column('id',db.Integer,primary_key=True)

    netid = db.Column('netid',db.String(50),unique=True,nullable=False)
    name = db.Column('name',db.String(100),nullable=False)
    email = db.Column('email',db.String(50),unique=True,nullable=False)
    bio = db.Column('bio',db.String(500),nullable=True)

    is_student = db.Column('is_student',db.Boolean,default=True)
    is_tutor = db.Column('is_tutor',db.Boolean,default=False)
    is_admin = db.Column('is_admin',db.Boolean,default=False)


    tutor_courses = db.relationship('TutorCourses', backref='tutor', lazy=True)

    def __init__(self, netid, name, email):
        self.netid = netid
        self.name = name
        self.email = email


    def __repr__(self):
        return '<id {}>'.format(self.id)

    # temporary manual serializer
    # to do (Ernest): use a package: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    def serialize(self):
        return {
            'id': self.id,
            'netid': self.netid,
            'name': self.name,
            'email': self.email,
            'bio': self.bio,
            'is_student': self.is_student,
            'is_tutor': self.is_tutor,
            'is_admin': self.is_admin,
        }


class Courses(db.Model):
    __tablename__ = 'courses'

    id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column('name',db.String(300),nullable=False)
    dept_course = db.Column('dept_course',db.String(100),nullable=False)

    tutor_courses = db.relationship('TutorCourses', backref='courses', lazy=True)
    tutorships = db.relationship('Tutorships', backref='courses', lazy=True)

    def __init__(self,name, dept_course):
        self.name = name
        self.dept_course = dept_course

    def __repr__(self):
        return '<id {}>'.format(self.id)

    # temporary manual serializer
    # to do (Ernest): use a package: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'dept_course': self.dept_course,
        }


class Tutorships(db.Model):
    __tablename__ = 'tutorships'

    id = db.Column('id',db.Integer,primary_key=True)
    status = db.Column('status',db.String(),nullable=False)

    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tutor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    student = db.relationship("Users", foreign_keys=[student_id])
    tutor = db.relationship("Users", foreign_keys=[tutor_id])

    course_id = db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))


    VALID_STATUS = ['requested', 'accepted', 'blocked', 'none']


    def __repr__(self):
        return '<id {}>'.format(self.id)

    def __init__(self, status, student_id, tutor_id, course_id):
        self.student_id = student_id
        self.tutor_id = tutor_id
        self.course_id = course_id
        self.status = status
        if status not in self.VALID_STATUS:
            raise Exception("Error: Invalid status given. Tutorships can have only one of the following statuses: " + str(self.VALID_STATUS))
        


    # temporary manual serializer
    # to do (Ernest): use a package: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    def serialize(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'tutor_id': self.tutor_id,
            'course_id': self.course_id,
            'status': self.status
        }



class TutorCourses(db.Model):
    __tablename__ = 'tutor_courses'

    id = db.Column('id',db.Integer,primary_key=True)

    tutor_id = db.Column('tutor_id', db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), nullable=False)
    status = db.Column('status',db.String(100),nullable=False)

    def __init__(self, tutor_id, course_id, status):
        self.tutor_id = tutor_id
        self.course_id = course_id
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

     # temporary manual serializer
    # to do (Ernest): use a package: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    def serialize(self):
        return {
            'id': self.id,
            'tutor_id': self.tutor_id,
            'course_id': self.course_id,
            'status': self.status
        }
