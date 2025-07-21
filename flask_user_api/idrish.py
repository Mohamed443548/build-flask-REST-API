from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory user store: id -> user data
users_db = {}
current_id = 1

# Helper: generate user response
def user_response(user):
    return {
        'id': user['id'],
        'name': user['name'],
        'email': user['email'],
        'created_at': user['created_at']
    }

# Route: Get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    return jsonify([user_response(u) for u in users_db.values()]), 200

# Route: Get user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users_db.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user_response(user)), 200

# Route: Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    global current_id
    data = request.get_json()

    if not data or not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email are required'}), 400

    new_user = {
        'id': current_id,
        'name': data['name'],
        'email': data['email'],
        'created_at': datetime.utcnow().isoformat()
    }

    users_db[current_id] = new_user
    current_id += 1
    return jsonify(user_response(new_user)), 201

# Route: Update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = users_db.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])

    return jsonify(user_response(user)), 200

# Route: Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users_db:
        return jsonify({'error': 'User not found'}), 404

    del users_db[user_id]
    return jsonify({'message': f'User {user_id} deleted successfully'}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
