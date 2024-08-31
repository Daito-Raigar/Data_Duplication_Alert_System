import os
import json
import shutil
import subprocess
from flask import Flask, request, jsonify, send_file, abort
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Directory where admin datasets are stored
ADMIN_DATASET_DIRECTORY = "C:/datasets"

# Directory where datasets should be shared with users
SHARED_DIRECTORY = "C:/SharedDatasets"

# Ensure the shared directory exists and is shared
def create_shared_directory():
    if not os.path.exists(SHARED_DIRECTORY):
        os.makedirs(SHARED_DIRECTORY)
        # Command to share the folder with full access for everyone
        share_command = f'net share SharedDatasets={SHARED_DIRECTORY} /grant:everyone,full'
        try:
            # Execute the command to share the folder
            subprocess.run(share_command, shell=True, check=True)
            print("Shared folder created and shared successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to share the folder: {e}")

# MongoDB connection details for the main database
MONGO_URI = "mongodb+srv://ddas:ddas@sample.nnpef.mongodb.net/?retryWrites=true&w=majority&appName=sample"
DATABASE_NAME = "ddas"
ADMIN_COLLECTION_NAME = "admin_details"
DOWNLOAD_COLLECTION_NAME = "already_downloaded_datasets"

# Connect to the main MongoDB database
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
admin_collection = db[ADMIN_COLLECTION_NAME]
download_collection = db[DOWNLOAD_COLLECTION_NAME]

# MongoDB connection details for the metadata database
METADATA_DATABASE_NAME = "Metadata"  # Name of the database where metadata is stored
METADATA_COLLECTION_NAME = "Metadata_collections"  # Collection where metadata is stored

# Connect to the metadata MongoDB database
metadata_db = client[METADATA_DATABASE_NAME]
metadata_collection = metadata_db[METADATA_COLLECTION_NAME]

def is_dataset_file(filename):
    # Filter out system files like 'desktop.ini'
    return not filename.startswith('.') and filename.lower() != 'desktop.ini'

def retrieve_metadata():
    return metadata_collection.find()

def create_file_from_metadata(metadata, file_path):
    with open(file_path, 'w') as file:
        json.dump(metadata, file, indent=4)
    print(f"Metadata written to {file_path}: {metadata}")

def create_datasets_from_metadata():
    if not os.path.exists(ADMIN_DATASET_DIRECTORY):
        os.makedirs(ADMIN_DATASET_DIRECTORY)
    
    metadata_cursor = retrieve_metadata()
    for index, metadata in enumerate(metadata_cursor):
        # Convert MongoDB BSON document to a Python dictionary
        metadata_dict = metadata if isinstance(metadata, dict) else metadata.to_dict()
        file_name = os.path.join(ADMIN_DATASET_DIRECTORY, f"dataset_{index+1}.json")
        create_file_from_metadata(metadata_dict, file_name)

def initialize():
    print("Initializing shared directory and datasets...")
    create_shared_directory()
    create_datasets_from_metadata()

@app.route('/api/metadata', methods=['POST'])
def get_metadata():
    try:
        metadata = list(retrieve_metadata())
        return jsonify(metadata)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin_datasets', methods=['POST'])
def list_admin_datasets():
    try:
        datasets = [f for f in os.listdir(ADMIN_DATASET_DIRECTORY) 
                    if os.path.isfile(os.path.join(ADMIN_DATASET_DIRECTORY, f)) 
                    and is_dataset_file(f)]
        return jsonify({'datasets': datasets})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shared_datasets', methods=['POST'])
def list_shared_datasets():
    try:
        datasets = [f for f in os.listdir(SHARED_DIRECTORY) 
                    if os.path.isfile(os.path.join(SHARED_DIRECTORY, f)) 
                    and is_dataset_file(f)]
        return jsonify({'datasets': datasets})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/check_admin/<filename>', methods=['POST'])
def check_admin_dataset(filename):
    try:
        admin_file_path = os.path.join(ADMIN_DATASET_DIRECTORY, filename)
        if os.path.exists(admin_file_path):
            return jsonify({'message': 'Dataset exists in admin directory.', 'exists': True}), 200
        return jsonify({'message': 'Dataset does not exist in admin directory.', 'exists': False}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/check_shared/<filename>', methods=['POST'])
def check_shared_dataset(filename):
    try:
        shared_file_path = os.path.join(SHARED_DIRECTORY, filename)
        if os.path.exists(shared_file_path):
            return jsonify({'message': 'Dataset exists in shared directory.', 'exists': True}), 200
        return jsonify({'message': 'Dataset does not exist in shared directory.', 'exists': False}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/check_all', methods=['POST'])
def check_all_datasets():
    try:
        datasets = os.listdir(ADMIN_DATASET_DIRECTORY)
        already_downloaded = []
        not_downloaded = []

        for filename in datasets:
            if is_dataset_file(filename):
                result = download_collection.find_one({'filename': filename})
                if result:
                    already_downloaded.append({
                        'filename': filename,
                        'client_ip': result['client_ip'],
                        'download_time': result.get('download_time', 'N/A'),
                        'dataset_path': os.path.join(SHARED_DIRECTORY, filename)
                    })
                else:
                    not_downloaded.append(filename)

        return jsonify({
            "already_downloaded": already_downloaded,
            "not_downloaded": not_downloaded
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>', methods=['POST'])
def download_dataset(filename):
    try:
        admin_file_path = os.path.join(ADMIN_DATASET_DIRECTORY, filename)
        shared_file_path = os.path.join(SHARED_DIRECTORY, filename)

        if os.path.exists(admin_file_path):
            # Copy file to shared directory if not already present
            if not os.path.exists(shared_file_path):
                shutil.copy2(admin_file_path, shared_file_path)
                
            result = download_collection.find_one({'filename': filename})
            if result:
                return jsonify({
                    "message": "Dataset already downloaded by another user.",
                    "downloaded": True,
                    "user_details": {
                        'client_ip': result['client_ip'],
                        'download_time': result.get('download_time', 'N/A'),
                        'dataset_path': shared_file_path
                    }
                }), 409

            # Insert record in MongoDB
            download_collection.insert_one({
                'filename': filename,
                'client_ip': request.remote_addr,
                'download_time': datetime.now(),
                'dataset_path': shared_file_path
            })

            return send_file(shared_file_path, as_attachment=True)
        return abort(404)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/datasets/<path:filename>', methods=['POST'])
def serve_file(filename):
    try:
        file_path = os.path.join(SHARED_DIRECTORY, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        return abort(404, description="File not found")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/log_download', methods=['POST'])
def log_download():
    try:
        data = request.json
        filename = data['filename']
        client_ip = request.remote_addr
        download_time = datetime.now()
        dataset_path = os.path.join(SHARED_DIRECTORY, filename)
        
        # Insert download details into the already_downloaded_datasets collection
        download_collection.insert_one({
            'filename': filename,
            'client_ip': client_ip,
            'download_time': download_time,
            'dataset_path': dataset_path
        })

        return jsonify({'message': 'Download logged successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to log admin details
@app.route('/api/log_admin', methods=['POST'])
def log_admin():
    try:
        data = request.json
        admin_details = {
            'admin_ip': request.remote_addr,
            'admin_name': data.get('admin_name', 'Unknown'),
            'log_time': datetime.now()
        }
        
        # Insert admin details into the admin_details collection
        admin_collection.insert_one(admin_details)

        return jsonify({'message': 'Admin details logged successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask app...")
    initialize() 
    app.run(host='192.168.74.42', port=5000, debug=True)
