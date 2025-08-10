from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage for users
users = {}
next_user_id = 1

# Helper function to validate user data
def validate_user_data(data, required_fields=None):
    if required_fields is None:
        required_fields = ['name', 'email']
    
    if not data:
        return False, "No data provided"
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"
    
    return True, None

# GET /users - Get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    """Retrieve all users"""
    return jsonify({
        'users': list(users.values()),
        'total': len(users)
    }), 200

# GET /users/<id> - Get specific user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a specific user by ID"""
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(users[user_id]), 200

# POST /users - Create new user
@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    global next_user_id
    
    data = request.json
    is_valid, error_msg = validate_user_data(data)
    
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    # Check if email already exists
    for user in users.values():
        if user['email'] == data['email']:
            return jsonify({'error': 'Email already exists'}), 400
    
    # Create new user
    new_user = {
        'id': next_user_id,
        'name': data['name'],
        'email': data['email'],
        'age': data.get('age'),
        'created_at': datetime.now().isoformat()
    }
    
    users[next_user_id] = new_user
    next_user_id += 1
    
    return jsonify(new_user), 201

# PUT /users/<id> - Update user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.json
    is_valid, error_msg = validate_user_data(data)
    
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    # Check if email already exists (excluding current user)
    for uid, user in users.items():
        if uid != user_id and user['email'] == data['email']:
            return jsonify({'error': 'Email already exists'}), 400
    
    # Update user
    users[user_id].update({
        'name': data['name'],
        'email': data['email'],
        'age': data.get('age'),
        'updated_at': datetime.now().isoformat()
    })
    
    return jsonify(users[user_id]), 200

# DELETE /users/<id> - Delete user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    
    deleted_user = users.pop(user_id)
    return jsonify({
        'message': 'User deleted successfully',
        'deleted_user': deleted_user
    }), 200

# Welcome endpoint
@app.route('/', methods=['GET'])
def welcome():
    """Welcome endpoint"""
    return jsonify({
        'message': 'Welcome to Flask User Management API',
        'endpoints': {
            'health': '/health',
            'users': '/users',
            'create_user': 'POST /users',
            'get_user': 'GET /users/<id>',
            'update_user': 'PUT /users/<id>',
            'delete_user': 'DELETE /users/<id>'
        }
    }), 200

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'total_users': len(users)
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Flask User Management API...")
    print("Available endpoints:")
    print("GET    /users         - Get all users")
    print("GET    /users/<id>    - Get specific user")
    print("POST   /users         - Create new user")
    print("PUT    /users/<id>    - Update user")
    print("DELETE /users/<id>    - Delete user")
    print("GET    /health        - Health check")
    print("\nServer running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
