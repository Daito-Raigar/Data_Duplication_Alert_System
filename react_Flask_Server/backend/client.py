import requests
import os

# Configuration
SERVER_URL = 'http://192.168.1.7:5000'  # Replace with your server's IP address
CLIENT_ID = 'client1'  # Example client ID
DOWNLOAD_DIR = './client_data/' + CLIENT_ID

# Create directory for the client
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def list_datasets():
    response = requests.get(f'{SERVER_URL}/api/datasets')
    if response.status_code == 200:
        datasets = response.json().get('datasets', [])
        print('Available datasets:')
        for dataset in datasets:
            print(dataset)
    else:
        print('Failed to fetch datasets.')

def check_dataset(filename):
    response = requests.get(f'{SERVER_URL}/api/check/{filename}')
    if response.status_code == 200:
        print('Dataset is not downloaded.')
        return False
    elif response.status_code == 409:
        print('Dataset already downloaded by another user.')
        return True
    else:
        print('Error checking dataset.')
        return False

def download_dataset(filename):
    response = requests.get(f'{SERVER_URL}/api/download/{filename}', stream=True)
    if response.status_code == 200:
        file_path = os.path.join(DOWNLOAD_DIR, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f'Dataset downloaded to {file_path}')
    elif response.status_code == 409:
        print('Dataset already downloaded by another user.')
    else:
        print('Error downloading dataset.')

def main():
    list_datasets()
    filename = input('Enter the filename to download: ')
    if not check_dataset(filename):
        download_dataset(filename)

if __name__ == '__main__': 
    main()
