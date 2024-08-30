from flask import Flask, request, jsonify, send_file, abort
import os
from pymongo import MongoClient
import io
import zipfile

app = Flask(__name__)

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

@app.route('/api/datasets', methods=['GET'])
def list_datasets():
    try:
        datasets = [f for f in os.listdir(DATASET_DIRECTORY) if os.path.isfile(os.path.join(DATASET_DIRECTORY, f))]
        print("Datasets listed:", datasets)  # Debug print
        return jsonify({'datasets': datasets})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/check/<filename>', methods=['GET'])
def check_dataset(filename):
    try:
        result = collection.find_one({'filename': filename})
        if result:
            return jsonify({'message': 'Dataset already downloaded.'}), 409
        return jsonify({'message': 'Dataset is not downloaded.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_dataset(filename):
    try:
        file_path = os.path.join(DATASET_DIRECTORY, filename)
        if os.path.exists(file_path):
            # Insert record in MongoDB
            collection.insert_one({'filename': filename, 'client_ip': request.remote_addr})
            return send_file(file_path, as_attachment=True)
        return abort(404)
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

        # Create an in-memory ZIP file
        memory_zip = io.BytesIO()
        with zipfile.ZipFile(memory_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in datasets:
                result = collection.find_one({'filename': filename})
                if result:
                    already_downloaded.append(filename)
                else:
                    file_path = os.path.join(DATASET_DIRECTORY, filename)
                    if os.path.exists(file_path):
                        zipf.write(file_path, filename)
                        collection.insert_one({'filename': filename, 'client_ip': request.remote_addr})
                        downloaded.append(filename)

        # Move the cursor to the beginning of the BytesIO object
        memory_zip.seek(0)

        return send_file(memory_zip, as_attachment=True, download_name="datasets.zip", mimetype='application/zip')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(host='192.168.74.42', port=5000, debug=True)  # Ensure this is different from server.py
