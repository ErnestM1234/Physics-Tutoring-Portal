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

    tutor_classes = db.relationship('TutorClasses', backref='tutor', lazy=True, primaryjoin="Users.id == TutorClasses.tutor_id")
    student_tutorships = db.relationship('Tutorships', backref='student', lazy=True, primaryjoin="Users.id == Tutorships.student_id")
    tutor_tutorships = db.relationship('Tutorships', backref='tutor', lazy=True, primaryjoin="Users.id == Tutorships.tutor_id")

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
    dept_course = db.Column('dept_course',db.String(100),nullable=False)

    tutor_classes = db.relationship('TutorClasses', backref='classes', lazy=True, primaryjoin="Classes.id == TutorClasses.class_id")
    tutorships = db.relationship('Tutorships', backref='classes', lazy=True, primaryjoin="Classes.id == Tutorships.class_id")

    def __init__(self, name, dept_course):
        self.name = name
        self.dept_course = dept_course

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def get_name(self):
        return self.name

    def get_dept_course(self):
        return self.dept_course


class Tutorships(db.Model):
    __tablename__ = 'tutorships'

    id = db.Column('id',db.Integer,primary_key=True)
    student_id = db.Column('student_id', db.Integer, db.ForeignKey(Users.id))
    tutor_id = db.Column('tutor_id', db.Integer, db.ForeignKey(Users.id))
    class_id = db.Column('class_id', db.Integer, db.ForeignKey(Classes.id))

    def __repr__(self):
        return '<id {}>'.format(self.id)


class TutorClasses(db.Model):
    __tablename__ = 'tutor_classes'

    id = db.Column('id',db.Integer,primary_key=True)

    tutor_id = db.Column('tutor_id', db.Integer, db.ForeignKey(Users.id), nullable=False)
    class_id = db.Column('class_id', db.Integer, db.ForeignKey(Classes.id), nullable=False)
    status = db.Column('status',db.String(100),nullable=False)

    def __init__(self, tutor_id, class_id, status):
        self.tutor_id = tutor_id
        self.class_id = class_id
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)