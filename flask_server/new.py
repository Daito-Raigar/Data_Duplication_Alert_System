from pymongo import MongoClient
import os

# MongoDB Atlas connection string (replace <username>, <password>, <cluster-url> with your credentials)
MONGO_URI = "mongodb+srv://ddas:ddas@sample.nnpef.mongodb.net/?retryWrites=true&w=majority&appName=sample"

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)

# Select your database and collection
db = client.download_tracking
downloads_collection = db.downloads

# Function to check if the dataset is already downloaded by the user
def check_dataset_download(user_id, dataset_name):
    download_record = downloads_collection.find_one({
        "user_id": user_id,
        "dataset_name": dataset_name
    })
    
    if download_record:
        return f"Dataset already downloaded. Access it here: {download_record['file_path']}"
    return None

# Function to record a new download
def record_dataset_download(user_id, dataset_name, file_path):
    downloads_collection.insert_one({
        "user_id": user_id,
        "dataset_name": dataset_name,
        "file_path": file_path
    })

# Function to simulate downloading a dataset
def download_dataset(user_id, dataset_name):
    # Simulate download process (in reality, this would be where the download occurs)
    # Here we just define a folder where datasets are stored
    file_path = f"/datasets/{user_id}/{dataset_name}.zip"
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Simulate creating the dataset file
    with open(file_path, "w") as file:
        file.write("This is the dataset content.")
    
    # Record the download
    record_dataset_download(user_id, dataset_name, file_path)
    
    return file_path

# Function to handle user request to download dataset
def handle_download_request(user_id, dataset_name):
    # Check if the dataset is already downloaded
    download_status = check_dataset_download(user_id, dataset_name)
    
    if download_status:
        return download_status
    else:
        # Proceed with downloading the dataset
        file_path = download_dataset(user_id, dataset_name)
        return f"Dataset has been downloaded to: {file_path}"

# Example usage:
user_id = "user123"
dataset_name = "sample_dataset"

result = handle_download_request(user_id, dataset_name)
print(result)