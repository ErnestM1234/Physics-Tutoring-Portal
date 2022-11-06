from app import app, db
from flask import jsonify, request
from src.database.models import Classes
from marshmallow import Schema, fields





""" GET /api/class/
Parameters:
    - id (int)!
"""
class GetClassInputSchema(Schema):
    id = fields.Integer(required=True)
get_class_input_schema = GetClassInputSchema()

@app.route('/api/class/', methods=['GET'])
def read_class():
    errors = get_class_input_schema.validate(request.args)
    if errors:
        return {"message": str(errors) }, 400
    
    try:
        id = request.args['id']
        course = Classes.query.filter(Classes.id == id).first()
        if course is None:
            return {"message": "Class could not be found."}, 400
    except Exception as e:
        return {"error": str(e)}, 400

    return jsonify(course.serialize())





""" GET /api/classes/
Parameters:
    - id            (int)?
    - name          (str)?
    - dept_course   (str)?
"""
class GetClassesInputSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    dept_course = fields.String()
get_classes_input_schema = GetClassesInputSchema()

@app.route('/api/classes/', methods=['GET'])
def get_classes():
    errors = get_classes_input_schema.validate(request.args)
    if errors:
        return {"message": str(errors) }, 400

    try:
        id = request.args.get('id')
        name = request.args.get('name')
        dept_course = request.args.get('dept_course')

        filter = []
        if id:
            filter.append(Classes.id == id)
        if name:
            filter.append(Classes.name == name)
        if dept_course:
            filter.append(Classes.dept_course == dept_course)
        classes = Classes.query.filter(*filter).all()
        return jsonify([course.serialize() for course in classes])
    except Exception as e:
        return {"error": str(e)}, 400





""" POST /api/class/create
Parameters:
    - name          (str)!
    - dept_course   (str)!
"""
class CreateClassInputSchema(Schema):
    name = fields.String(required=True)
    dept_course = fields.String(required=True)
create_class_input_schema = CreateClassInputSchema()

@app.route('/api/class/create', methods=['POST'])
def create_class():
    errors = create_class_input_schema.validate(request.form)
    if errors:
        return {"message": str(errors) }, 400
    
    try:
        course = Classes(request.form['name'], request.form['dept_course'])
        db.session.add(course)
        db.session.commit()
        return {"message": "success" }, 200
    except Exception as e:
        return {"error": str(e)}, 400




""" POST /api/class/update
Parameters:
    - id            (int)!
    - name          (str)?
    - dept_course   (str)?
"""
class UpdateClassInputSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String()
    dept_course = fields.String()
update_class_input_schema = UpdateClassInputSchema()

@app.route('/api/class/update', methods=['POST'])
def  update_class():
    errors = update_class_input_schema.validate(request.form)
    if errors:
        return {"message": str(errors) }, 400
    
    try:
        id = request.form['id']
        course = Classes.query.filter(Classes.id == id).first()
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





""" POST /api/class/
Parameters:
    - id (int)!
"""
class DeleteClassInputSchema(Schema):
    id = fields.Integer(required=True)
delete_class_input_schema = DeleteClassInputSchema()

@app.route('/api/class/delete', methods=['POST'])
def delete_class():
    errors = delete_class_input_schema.validate(request.form)
    if errors:
        return {"message": str(errors) }, 400

    try:
        id = request.form['id']
        course = Classes.query.filter(Classes.id == id).first()
        if course is None:
            return {"message": "Class could not be found."}, 400
        db.session.delete(course)
        db.session.commit()
        return {"message": "success" }, 200
    except Exception as e:
        return {"error": str(e)}, 400
