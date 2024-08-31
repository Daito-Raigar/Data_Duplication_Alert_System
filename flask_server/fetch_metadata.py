import os
import pandas as pd
import json
import xml.etree.ElementTree as ET
from docx import Document
from pymongo import MongoClient

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://ddas:ddas@sample.nnpef.mongodb.net/?retryWrites=true&w=majority&appName=sample")

# Select the database and collection
db = client["Metadata"]
collection = db["Metadata_collection"]

# Extract metadata for CSV files
def extract_metadata_csv(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    df = pd.read_csv(file_path)
    num_rows, num_columns = df.shape
    
    metadata = {
        "dataset_name": file_name,
        "file_location": file_path,
        "size_bytes": file_size,
        "num_rows": num_rows,
        "num_columns": num_columns,
        "upload_date": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return metadata

# Extract metadata for Word files
def extract_metadata_docx(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    doc = Document(file_path)
    num_paragraphs = len(doc.paragraphs)
    
    metadata = {
        "dataset_name": file_name,
        "file_location": file_path,
        "size_bytes": file_size,
        "num_paragraphs": num_paragraphs,
        "upload_date": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return metadata

# Extract metadata for XML files
def extract_metadata_xml(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    tree = ET.parse(file_path)
    root = tree.getroot()
    num_elements = len(list(root.iter()))
    
    metadata = {
        "dataset_name": file_name,
        "file_location": file_path,
        "size_bytes": file_size,
        "num_elements": num_elements,
        "upload_date": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return metadata

# Extract metadata for JSON files
def extract_metadata_json(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    with open(file_path, 'r') as f:
        data = json.load(f)
    num_elements = len(data)
    
    metadata = {
        "dataset_name": file_name,
        "file_location": file_path,
        "size_bytes": file_size,
        "num_elements": num_elements,
        "upload_date": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return metadata

# Upload metadata to MongoDB
def upload_metadata(metadata):
    if metadata:
        try:
            # Check if metadata for this file already exists
            existing_metadata = collection.find_one({"dataset_name": metadata['dataset_name']})
            if existing_metadata:
                print(f"Metadata for {metadata['dataset_name']} already exists.")
            else:
                collection.insert_one(metadata)
                print(f"Uploaded metadata for: {metadata['dataset_name']}")
        except Exception as e:
            print(f"Error uploading metadata: {e}")
# Scan directory for files
def scan_directory(directory_path):
    datasets = {}
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if file_name.endswith('.csv'):
            datasets[file_name] = (file_path, extract_metadata_csv)
        elif file_name.endswith('.docx'):
            datasets[file_name] = (file_path, extract_metadata_docx)
        elif file_name.endswith('.xml'):
            datasets[file_name] = (file_path, extract_metadata_xml)
        elif file_name.endswith('.json'):
            datasets[file_name] = (file_path, extract_metadata_json)
    return datasets

# Process all datasets in the specified directory
def process_directory_datasets(directory_path):
    datasets = scan_directory(directory_path)
    if not datasets:
        print("No supported files found in the directory.")
    for dataset_name, (file_path, metadata_function) in datasets.items():
        print(f"Processing dataset: {dataset_name} at {file_path}")
        metadata = metadata_function(file_path)
        upload_metadata(metadata)

# Example usage
directory_path = 'D:/ML Tutorials'  # Update with the correct directory path
process_directory_datasets(directory_path)

# Verify upload
print("Documents in MongoDB:")
for doc in collection.find():
    print(doc)