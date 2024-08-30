// src/components/Sidebar.js
import React from 'react';
import { List, ListItem, ListItemText, Divider, Typography } from '@mui/material';
import { Link } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
    return (
        <div className="sidebar-container">
            <Typography variant="h6" className="sidebar-title">
                Dashboard
            </Typography>
            <List component="nav">
                <ListItem button component={Link} to="/settings" className="sidebar-item">
                    <ListItemText primary="Settings" />
                </ListItem>
                <Divider className="sidebar-divider" />
                <ListItem button component={Link} to="/collab-work" className="sidebar-item">
                    <ListItemText primary="Collab Work" />
                </ListItem>
                <Divider className="sidebar-divider" />
                <ListItem button component={Link} to="/upgrade" className="sidebar-item">
                    <ListItemText primary="Upgrade" />
                </ListItem>
                <Divider className="sidebar-divider" />
                <ListItem button component={Link} to="/profile" className="sidebar-item">
                    <ListItemText primary="User Profile" />
                </ListItem>
            </List>
        </div>
    );
};

export default Sidebar;
