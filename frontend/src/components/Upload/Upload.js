import React, { useState } from 'react';
import './Upload.css'

const UploadPage = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [fileMetadata, setFileMetadata] = useState({});

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setSelectedFile(file);
            getFileMetadata(file);
        }
    };

    const getFileMetadata = (file) => {
        // Create a FileReader to read the file
        const reader = new FileReader();
        reader.onload = () => {
            const fileContent = reader.result;
            // Assuming you are only handling text-based files for simplicity
            const metadata = {
                name: file.name,
                size: file.size,
                type: file.type,
                lastModified: file.lastModified
            };
            setFileMetadata(metadata);
        };
        reader.readAsArrayBuffer(file); // Or use other methods depending on file type
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            alert("No file selected");
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch('http://localhost:5000/api/upload', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                alert('File successfully uploaded');
            } else {
                alert('Failed to upload file');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <h1>Upload Page</h1>
            <input type="file" onChange={handleFileChange} />
            {selectedFile && (
                <div>
                    <h2>File Metadata:</h2>
                    <p>Name: {fileMetadata.name}</p>
                    <p>Size: {fileMetadata.size} bytes</p>
                    <p>Type: {fileMetadata.type}</p>
                    <p>Last Modified: {new Date(fileMetadata.lastModified).toLocaleString()}</p>
                    <button onClick={handleUpload}>Upload</button>
                </div>
            )}
        </div>
    );
};

export default UploadPage;
