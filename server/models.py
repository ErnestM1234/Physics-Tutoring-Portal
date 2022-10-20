# this is a file containing our datamodels

from app import db

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column('id',db.Integer,primary_key=True)

    netid = db.Column('netid',db.String(50),unique=True,nullable=False)
    name = db.Column('name',db.String(100),nullable=False)
    email = db.Column('email',db.String(50),unique=True,nullable=False)
    bio = db.Column('bio',db.String(500),nullable=True)

    isStudent = db.Column('is_student',db.Boolean,default=True)
    isTutor = db.Column('is_tutor',db.Boolean,default=False)
    isAdmin = db.Column('is_admin',db.Boolean,default=False)


    def __init__(self, netid, name, email):
        self.netid = netid
        self.name = name
        self.email = email


    def __repr__(self):
        return '<id {}>'.format(self.id)



class Classes(db.Model):
    __tablename__ = 'classes'

    id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column('name',db.String(300),nullable=False)
    dept_course = db.Column('name',db.String(100),nullable=False)

    def __init__(self,name, dept_course):
        self.name = name
        self.dept_course = dept_course

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Tutorships(db.Model):
    __tablename__ = 'tutorships'

    id = db.Column('id',db.Integer,primary_key=True)
    student_id = db.Column('student_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    tutor_id = db.Column('tutor_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    class_id = db.Column('class_id', db.Integer, db.ForeignKey('classes.id'), primary_key=True)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class TutorClass(db.Model):
    __tablename__ = 'tutor_classes'

    id = db.Column('id',db.Integer,primary_key=True)

    tutor_id = db.Column('tutor_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    class_id = db.Column('class_id', db.Integer, db.ForeignKey('classes.id'), primary_key=True)
    status = db.Column('status',db.String(100),nullable=False)

    def __init__(self, tutor_id, class_id, status):
        self.tutor_id = tutor_id
        self.class_id = class_id
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)
