from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

from fetch_metadata import process_directory_datasets

app = Flask(__name__)
CORS(app)  # To handle CORS errors when making requests from React

# MongoDB connection
client = MongoClient("mongodb+srv://ddas:ddas@sample.nnpef.mongodb.net/?retryWrites=true&w=majority&appName=sample")

# Select the database and collection
db = client["Metadata"]
collection = db["Metadata_collection"]

# Route to get all metadata
@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    metadata_list = list(collection.find({}, {'_id': 0}))  # Exclude the MongoDB '_id' field
    return jsonify(metadata_list)

# Route to get metadata by file name
@app.route('/api/metadata/<string:filename>', methods=['GET'])
def get_metadata_by_filename(filename):
    metadata = collection.find_one({"dataset_name": filename}, {'_id': 0})
    if metadata:
        return jsonify(metadata)
    else:
        return jsonify({"error": "Metadata not found"}), 404

# Route to trigger processing of a directory (for example, a button in the React app could call this)
@app.route('/api/process_directory', methods=['POST'])
def process_directory():
    directory_path = request.json.get('directory_path')
    if directory_path:
        process_directory_datasets(directory_path)
        return jsonify({"message": "Directory processed successfully"})
    else:
        return jsonify({"error": "Directory path is required"}), 400

if __name__ == '__main__':
    app.run(debug=True)