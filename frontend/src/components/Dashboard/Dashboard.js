import React, { useEffect, useState } from 'react';
import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography } from '@mui/material';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
    const [datasets, setDatasets] = useState([]);

    useEffect(() => {
        // Fetch the metadata from the Flask API
        axios.get('http://localhost:5000/api/metadata')
            .then(response => {
                setDatasets(response.data);
            })
            .catch(error => {
                console.error("There was an error fetching the metadata!", error);
            });
    }, []);

    const download = (filename) => {
        // Create a link element
        const link = document.createElement('a');
        link.href = `http://localhost:5000/api/download/${filename}`;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div className="dashboard-container">
            <Typography variant="h4" className="dashboard-title">
                Datasets
            </Typography>
            <div className="dashboard-buttons">
                <Link to="/login" style={{ textDecoration: 'none' }}>
                    <Button variant="contained" color="primary" className="dashboard-button">
                        Login
                    </Button>
                </Link>
                <Link to="/signup" style={{ textDecoration: 'none' }}>
                    <Button variant="contained" color="secondary" className="dashboard-button">
                        Signup
                    </Button>
                </Link>
            </div>
            <TableContainer component={Paper} className="dashboard-table-container">
                <Table>
                    <TableHead>
                        <TableRow className="dashboard-table-header">
                            <TableCell className="dashboard-table-header-cell">Name</TableCell>
                            <TableCell className="dashboard-table-header-cell" align="right">Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {datasets.map((dataset) => (
                            <TableRow key={dataset.dataset_name}>
                                <TableCell component="th" scope="row">
                                    {dataset.dataset_name}
                                </TableCell>
                                <TableCell align="right">
                                    <Button variant="contained" color="primary" className="dashboard-button">View</Button>
                                    <Button variant="contained" color="secondary" className="dashboard-button" onClick={() =>download(dataset.dataset_name)}>Download</Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    );
};

export default Dashboard;