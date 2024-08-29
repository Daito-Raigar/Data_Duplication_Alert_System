from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['db'] 
users_collection = db['User_Details'] 

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

    # Check if the user exists and password matches
    user = users_collection.find_one({"email": data["email"]})
    if user and user["password"] == data["password"]:
        return jsonify({"message": "Login successful", "user": user})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)