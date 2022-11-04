from app import app, db
from flask import jsonify, request
from src.database.models import Users
from marshmallow import Schema, fields




""" GET /api/user/
Parameters:
    - id (int)!
"""
class GetUserInputSchema(Schema):
    id = fields.Integer(required=True)
get_user_input_schema = GetUserInputSchema()

@app.route('/api/user/', methods=['GET'])
def get_user():
    errors = get_user_input_schema.validate(request.args)
    if errors:
        return {"message": str(errors) }, 400
    
    try:
        id = request.args['id']
        user = Users.query.filter(Users.id == id).first()
        if user is None:
            return {"message": "User could not be found."}, 400
    except Exception as e:
        return {"error": str(e)}, 400

    if user is None:
        return {"message": "No user with id " + str(id) + " exists."}

    return jsonify(user.serialize())




""" GET /api/users/
Parameters:
    - netid        (str)
    - email        (str)
    - is_student   (bool)
    - is_tutor     (bool)
    - is_admin     (bool)
"""
class GetUsersInputSchema(Schema):
    id = fields.Integer()
    netid = fields.String()
    name = fields.String()
    email = fields.String()
    is_student = fields.Boolean()
    is_tutor = fields.Boolean()
    is_admin = fields.Boolean()
get_users_input_schema = GetUsersInputSchema()

@app.route('/api/users/', methods=['GET'])
def get_users():
    errors = get_users_input_schema.validate(request.args)
    if errors:
        return {"message": str(errors) }, 400

    try:
        users = Users.query.all()
        return jsonify([user.serialize() for user in users])
    except Exception as e:
        return {"error": str(e)}, 400




""" POST /api/user/create/
Parameters:
    - name  (string)!
    - netid (string)!
    - email (string)!
"""
class CreateUserInputSchema(Schema):
    netid = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
create_user_input_schema = CreateUserInputSchema()

@app.route('/api/user/create', methods=['POST'])
def create_user():
    errors = create_user_input_schema.validate(request.form)
    if errors:
        return {"message": str(errors) }, 400
    
    try:
        user = Users(request.form['netid'], request.form['name'], request.form['email'])
        db.session.add(user)
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

@app.route('/api/user/update', methods=['POST'])
def  update_user():
    errors = update_user_input_schema.validate(request.form)
    if errors:
        return {"message": str(errors) }, 400

    try:
        id = request.form['id']
        user = Users.query.filter(Users.id == id).first()
        if user is None:
            return {"message": "User could not be found."}, 400
        # todo (Ernest): find if there is a better way to do this
        if request.form['netid'] not in [None, '']:
            user.netid = request.form['netid']
        if request.form['name'] not in [None, '']:
            user.name = request.form['name']
        if request.form['email'] not in [None, '']:
            user.email = request.form['email']
        if request.form['bio'] not in [None, '']:
            user.bio = request.form['bio']
        if request.form['is_student'] not in [None, '']:
            user.is_student = request.form['is_student']
        if request.form['is_tutor'] not in [None, '']:
            user.is_tutor = request.form['is_tutor']
        if request.form['is_admin'] not in [None, '']:
            user.is_admin = request.form['is_admin']
        db.session.commit()
        return {"message": "success" }, 200
    except Exception as e:
        return {"error": str(e)}, 400




""" POST /api/user/delete
Parameters:
    - id (int)!
"""
class DeleteUserInputSchema(Schema):
    id = fields.String(required=True)
delete_user_input_schema = DeleteUserInputSchema()

@app.route('/api/user/delete', methods=['POST'])
def delete_user():
    errors = delete_user_input_schema.validate(request.form)
    if errors:
        return {"message": str(errors) }, 400

    try:
        id = request.form['id']
        user = Users.query.filter(Users.id == id).first()
        if user is None:
            return {"message": "User could not be found."}, 400
        db.session.delete(user)
        db.session.commit()
        return {"message": "success" }, 200
    except Exception as e:
        return {"error": str(e)}, 400
