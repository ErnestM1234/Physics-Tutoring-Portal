from app import app

@app.route('/api/class_tutor/', methods=['GET'])
def class_tutor():
    return 'read class_tutor'

@app.route('/api/class_tutor/create', methods=['POST'])
def create_class_tutor():
    return 'create class_tutor'

@app.route('/api/class_tutor/update', methods=['POST'])
def  update_class_tutor():
    return 'update class_tutor'

@app.route('/api/class_tutor/delete', methods=['POST'])
def delete_class_tutor():
    return 'delete class_tutor'
