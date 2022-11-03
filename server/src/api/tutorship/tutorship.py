from app import app

@app.route('/api/tutorship/', methods=['GET'])
def tutorship():
    return 'read tutorship'

@app.route('/api/tutorship/create', methods=['POST'])
def create_tutorship():
    return 'create tutorship'

@app.route('/api/tutorship/update', methods=['POST'])
def  update_tutorship():
    return 'update tutorship'

@app.route('/api/tutorship/delete', methods=['POST'])
def delete_tutorship():
    return 'delete tutorship'
