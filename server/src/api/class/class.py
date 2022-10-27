from app import app

@app.route('/api/class/', methods=['GET'])
def read_class():
    return 'read class'

@app.route('/api/class/create', methods=['POST'])
def create_class():
    return 'create class'

@app.route('/api/class/update', methods=['POST'])
def  update_class():
    return 'update class'

@app.route('/api/class/delete', methods=['POST'])
def delete_class():
    return 'delete class'
