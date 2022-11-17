from app import app, db
from flask import jsonify, request
from src.database.models import Users
from marshmallow import Schema, fields
import json




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
        id = request.args.get('id')
        user = Users.query.filter(Users.id == id).first()
        if user is None:
            return {"message": "User could not be found."}, 400
        return jsonify(user.serialize())
    except Exception as e:
        return {"error": str(e)}, 400




""" GET /api/users/
Parameters:
    - netid        (str)?
    - email        (str)?
    - is_student   (bool)?
    - is_tutor     (bool)?
    - is_admin     (bool)?
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
        id = request.args.get('id')
        netid = request.args.get('netid')
        name = request.args.get('name')
        email = request.args.get('email')
        is_student = request.args.get('is_student')
        is_tutor = request.args.get('is_tutor')
        is_admin = request.args.get('is_admin')

        filters = []
        if id:
            filters.append(Users.id == id)
        if netid:
            filters.append(Users.netid == netid)
        if name:
            filters.append(Users.name == name)
        if email:
            filters.append(Users.email == email)
        if is_student:
            filters.append(Users.is_student == is_student)
        if is_tutor:
            filters.append(Users.is_tutor == is_tutor)
        if is_admin:
            filters.append(Users.is_admin == is_admin)

        users = Users.query.filter(*filters).all()
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
    data = json.loads(request.data)
    errors = create_user_input_schema.validate(data)
    if errors:
        return {"message": str(errors) }, 400
    
    try:
        user = Users(data.get('netid'), data.get('name'), data.get('email'))
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
    data = json.loads(request.data)
    errors = update_user_input_schema.validate(data)
    if errors:
        return {"message": str(errors) }, 400

    try:
        id = data.get('id')
        user = Users.query.filter(Users.id == id).first()
        if user is None:
            return {"message": "User could not be found."}, 400
        # todo (Ernest): find if there is a better way to do this
        if data.get('netid') not in [None, '']:
            user.netid = data.get('netid')
        if data.get('name') not in [None, '']:
            user.name = data.get('name')
        if data.get('email') not in [None, '']:
            user.email = data.get('email')
        if data.get('bio') not in [None, '']:
            user.bio = data.get('bio')
        if data.get('is_student') not in [None, '']:
            user.is_student = data.get('is_student')
        if data.get('is_tutor') not in [None, '']:
            user.is_tutor = data.get('is_tutor')
        if data.get('is_admin') not in [None, '']:
            user.is_admin = data.get('is_admin')
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
    data = json.loads(request.data)
    errors = delete_user_input_schema.validate(data)
    if errors:
        return {"message": str(errors) }, 400

    try:
        id = data.get('id')
        user = Users.query.filter(Users.id == id).first()
        if user is None:
            return {"message": "User could not be found."}, 400
        db.session.delete(user)
        db.session.commit()
        return {"message": "success" }, 200
    except Exception as e:
        return {"error": str(e)}, 400
