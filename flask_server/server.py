from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from pymongo import MongoClient

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

# Connect to MongoDB
client = MongoClient('mongodb+srv://ddas:ddas@sample.nnpef.mongodb.net/?retryWrites=true&w=majority&appName=sample')
db = client['Metadata'] 
users_collection = db['user_details_collection'] 

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json  # Get JSON data from the request

    # Check if the user already exists
    if users_collection.find_one({"email": data["email"]}):
        return jsonify({"message": "User already exists"}), 409

    # Insert new user data into the database
    users_collection.insert_one(data)
    return jsonify({"message": "User registered successfully"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json  # Get JSON data from the request
    username = data.get('username')
    password = data.get('password')
    print(username,"and ", password)
    # Check if the user exists and password matches
    user = users_collection.find_one({"username": username })
    if user and user["password"] == password:
        user["_id"] = str(user["_id"])
        id = str(user["_id"])
        print(id)
        return jsonify({"message": "Login successful", "user": id})
    else:
        return jsonify({"message": "Invalid credentials", "success": False}), 401

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('response', {'data': 'Connected to WebSocket server'})

#@socketio.on('disconnect')
#def handle_disconnect():
   # print("Client disconnected")

@socketio.on('message')
def handle_message(data):
    print('Message received:', data)
    emit('response', {'data': 'Message received'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)