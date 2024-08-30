import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Set your API URL here
const API_URL = 'http://192.168.1.7:5000'; // Replace <YOUR_LOCAL_IP> with your local machine IP address

function DatasetDownloader() {
  const [datasets, setDatasets] = useState([]);
  const [alertMessage, setAlertMessage] = useState('');

  useEffect(() => {
    async function fetchDatasets() {
      try {
        const response = await axios.get(`${API_URL}/datasets`);
        setDatasets(response.data.datasets);
      } catch (error) {
        console.error('Error fetching datasets:', error);
      }
    }
    fetchDatasets();
  }, []);

  const downloadDataset = async (filename) => {
    try {
      const response = await axios.get(`${API_URL}/download/${filename}`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);  // Filename with extension
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Error downloading dataset:', error);
      setAlertMessage('Error downloading the dataset.');
    }
  };

  return (
    <div>
      <h1>Datasets</h1>
      <ul>
        {datasets.map((dataset) => (
          <li key={dataset}>
            {dataset}
            <button onClick={() => downloadDataset(dataset)}>Download</button>
          </li>
        ))}
      </ul>
      {alertMessage && <div className="alert">{alertMessage}</div>}
    </div>
  );
}

export default DatasetDownloader;
