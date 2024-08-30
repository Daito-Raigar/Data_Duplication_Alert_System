import React, { useEffect, useState } from 'react';
import DatasetDownloader from './components/DatasetDownloader';

const API_URL = 'http://192.168.1.7:5000'; // Replace <YOUR_LOCAL_IP> with your local machine IP address

const App = () => {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);

  // Async function to fetch data from the API
  async function fetchData() {
    try {
      const response = await fetch(`${API_URL}/get`); // Fetch data from Flask API
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const result = await response.json(); // Parse JSON response
      setData(result);
    } catch (error) {
      setError(error);
      console.error('Error fetching data:', error);
    }
  }

  // Call fetchData on component mount
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="App">
      <h1>Data from Flask API</h1>
      {error && <p>Error: {error.message}</p>}
      <ul>
        {data.map((item, index) => (
          <li key={index}>
            <p>Name: {item.name}</p>
          </li>
        ))}
      </ul>
      <DatasetDownloader />
    </div>
  );
}

export default App;
