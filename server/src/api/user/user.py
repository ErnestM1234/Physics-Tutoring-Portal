from app import app

@app.route('/api/user/', methods=['GET'])
def user():
    return 'read user'

@app.route('/api/user/create', methods=['POST'])
def create_user():
    return 'create user'

@app.route('/api/user/update', methods=['POST'])
def  update_user():
    return 'update user'

@app.route('/api/user/delete', methods=['POST'])
def delete_user():
    return 'delete user'
