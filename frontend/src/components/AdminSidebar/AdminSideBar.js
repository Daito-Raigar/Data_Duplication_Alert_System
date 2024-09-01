import React from 'react';
import '../AdminSidebar.css'; // Import the CSS for styling

const AdminSidebar = () => {
    return (
        <div className="ad-sidebar">
            <ul>
                <li>User Profile</li>
                <li>Database</li>
                <li>User Access Management</li>
            </ul>
        </div>
    );
}

export default AdminSidebar;
