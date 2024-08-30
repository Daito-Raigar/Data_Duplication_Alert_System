from flask import Flask, request, jsonify, send_file
import os
from pymongo import MongoClient

app = Flask(__name__)  # Corrected from _name to _name_

# Directory where datasets are stored
DATASET_DIRECTORY = "./datasets"

# MongoDB connection details
MONGO_URI = "mongodb+srv://ddas:ddas@sample.nnpef.mongodb.net/?retryWrites=true&w=majority&appName=sample"
DATABASE_NAME = "ddas"
COLLECTION_NAME = "sample"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

@app.route('/api/create_repository', methods=['POST'])
def create_repository():
    try:
        client_ip = request.remote_addr
        if client_ip:
            # Create a unique directory for each client based on their IP
            client_repo_path = os.path.join(DATASET_DIRECTORY, client_ip)
            if not os.path.exists(client_repo_path):
                os.makedirs(client_repo_path)
                return jsonify({"message": "Repository created successfully!"}), 201
            return jsonify({"message": "Repository already exists!"}), 200
        return jsonify({"message": "Failed to create repository."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/datasets', methods=['GET'])
def list_datasets():
    try:
        datasets = [f for f in os.listdir(DATASET_DIRECTORY) if os.path.isfile(os.path.join(DATASET_DIRECTORY, f))]
        return jsonify({'datasets': datasets})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/check_all', methods=['GET'])
def check_all_datasets():
    try:
        datasets = os.listdir(DATASET_DIRECTORY)
        already_downloaded = []
        not_downloaded = []

        for filename in datasets:
            result = collection.find_one({'filename': filename})
            if result:
                already_downloaded.append(filename)
            else:
                not_downloaded.append(filename)

        return jsonify({
            "already_downloaded": already_downloaded,
            "not_downloaded": not_downloaded
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download_all', methods=['GET'])
def download_all_datasets():
    try:
        datasets = os.listdir(DATASET_DIRECTORY)
        downloaded = []
        already_downloaded = []

        for filename in datasets:
            result = collection.find_one({'filename': filename})
            if result:
                already_downloaded.append(filename)
            else:
                dataset_path = os.path.join(DATASET_DIRECTORY, filename)
                if os.path.exists(dataset_path):
                    # Insert record in MongoDB
                    collection.insert_one({'filename': filename, 'client_ip': request.remote_addr})
                    downloaded.append(filename)

        return jsonify({
            "downloaded": downloaded,
            "already_downloaded": already_downloaded
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='192.168.1.7', port=5001, debug=True)