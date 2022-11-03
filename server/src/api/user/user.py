from app import app, db
from flask import jsonify, request
from src.database.models import Users


@app.route('/api/user/', methods=['GET'])
def get_user():
    return 'read user'

@app.route('/api/users/', methods=['GET'])
def get_users():
    if request.method == "GET":
        users = Users.query.all()
        # return users.serialize
        return jsonify([user.serialize() for user in users])
    else:
        return {"message": "failure"}
"""
POST /api/user/create
arguments:
    name string!
    netid string!
    email string!

    bio string?
    is_student boolean?
    is_tutor boolean?
    is_admin boolean?
returns:
    status 200
"""
@app.route('/api/user/create', methods=['POST'])
def create_user():
    if request.method == "POST":
        # todo: parameter validatoin
        user = Users(request.form['netid'], request.form['name'], request.form['email'])
        try:
            db.session.add(user)
            db.session.commit()
            return 'created user'
        except Exception:
            return str(Exception)
    else:
        return {"message": "failure"}

"""
POST /api/user/create
arguments:
    name string?
    netid string?
    email string?

    bio string?
    is_student boolean?
    is_tutor boolean?
    is_admin boolean?
returns:
    status 200
"""
@app.route('/api/user/update', methods=['POST'])
def  update_user():
    id = request.form['id']
    return 'update user'

@app.route('/api/user/delete', methods=['POST'])
def delete_user():
    id = request.form['id']
    return 'delete user'
