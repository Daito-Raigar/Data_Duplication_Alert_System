from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from docx import Document
from lxml import etree
import json
import os
import hashlib
import datetime
import py7zr  # For handling 7z compressed files

app = Flask(__name__)
CORS(app)  # To allow cross-origin requests

# MongoDB Atlas connection
client = MongoClient('mongodb+srv://ddas:ddas@sample.nnpef.mongodb.net/?retryWrites=true&w=majority&appName=sample')
db = client['Metadata']
collection = db['Metadata_collection']

def get_file_metadata(file_path):
    try:
        stat_info = os.stat(file_path)
        return {
            "creationDate": datetime.datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
            "lastModifiedDate": datetime.datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
            "filePath": file_path,
            "filePermissions": oct(stat_info.st_mode)[-3:],
            "fileOwner": stat_info.st_uid,
            "fileSize": stat_info.st_size,
            "checksumMD5": compute_checksum(file_path, 'md5'),
            "checksumSHA1": compute_checksum(file_path, 'sha1')
        }
    except Exception as e:
        return {"error": str(e)}

def compute_checksum(file_path, algo):
    hash_func = hashlib.md5() if algo == 'md5' else hashlib.sha1()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def get_docx_metadata(file):
    doc = Document(file)
    num_paragraphs = len(doc.paragraphs)
    return {"type": "docx", "paragraphs": num_paragraphs}

def get_xml_metadata(file):
    try:
        tree = etree.parse(file)
        root = tree.getroot()
        num_elements = len(root.findall('.//*'))
        return {"type": "xml", "elements": num_elements}
    except Exception as e:
        return {"type": "xml", "error": str(e)}

def get_json_metadata(file):
    try:
        data = json.load(file)
        num_keys = len(data) if isinstance(data, dict) else len(data)
        return {"type": "json", "keys": num_keys}
    except Exception as e:
        return {"type": "json", "error": str(e)}

def get_compression_info(file_path):
    try:
        with py7zr.SevenZipFile(file_path, 'r') as archive:
            compressed_size = sum([entry.size for entry in archive.list()])  # Example of compression info
        return {"compression": "7z", "compressedSize": compressed_size}
    except Exception as e:
        return {"compression": "unknown", "error": str(e)}

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    upload_folder = 'uploads'
    file_path = os.path.join(upload_folder, file.filename)
    
     # Ensure the 'uploads/' directory exists
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    # Save the file to a temporary location
    file.save(file_path)
    
    if file.filename.endswith('.7z'):
        compression_info = get_compression_info(file_path)
    else:
        compression_info = {"compression": "none"}

    # Extract metadata
    file_metadata = {
        "name": file.filename,
        "size": len(file.read()),
        "type": file.content_type,
        "lastModified": request.form.get('lastModified', 'Unknown'),
        **get_file_metadata(file_path),
        **compression_info
    }
    
    # Extract specific metadata based on file type
    if file.content_type == 'application/json':
        file_metadata.update(get_json_metadata(file))
    elif file.content_type == 'application/xml':
        file_metadata.update(get_xml_metadata(file))
    elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        file_metadata.update(get_docx_metadata(file))
    # Add more types as needed
    
    collection.insert_one(file_metadata)

    return jsonify({"message": "File successfully uploaded"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)