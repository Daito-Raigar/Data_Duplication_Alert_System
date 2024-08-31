from flask import Flask, request, jsonify
import hashlib
import os
import pymongo
import requests
from pymongo import MongoClient
from threading import Thread

app = Flask(__name__)

# MongoDB configuration
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['dataset_db']
collection = db['dataset_metadata']

def check_duplicate(file_hash):
    """Check if the file hash exists in MongoDB."""
    return collection.find_one({'hash': file_hash}) is not None

def process_dataset(url):
    """Process the dataset: check for duplicates and download if new."""
    try:
        # Calculate hash of the dataset
        response = requests.get(url, stream=True)
        hash_function = hashlib.md5()
        for chunk in response.iter_content(chunk_size=8192):
            hash_function.update(chunk)
        file_hash = hash_function.hexdigest()

        # Check for duplicates
        if check_duplicate(file_hash):
            print(f"Duplicate file detected and skipped: {url}")
        else:
            # Save metadata to MongoDB
            collection.insert_one({'url': url, 'hash': file_hash})
            # Download the file
            file_path = os.path.join("E:\DDAS\Downloads", os.path.basename(url))  # Local directory path
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"File downloaded and processed for URL: {url}")
            print(f"ALERT: New file downloaded: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/process-dataset', methods=['POST'])
def process_dataset_endpoint():
    """Endpoint to process the dataset request."""
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"message": "URL is required"}), 400
    
    # Start the dataset processing in a separate thread
    Thread(target=process_dataset, args=(url,)).start()
    
    return jsonify({"message": "Processing started, check logs for details."})

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        file_path = os.path.join('uploads', filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
