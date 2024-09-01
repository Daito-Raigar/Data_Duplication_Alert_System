import React from 'react';
 import AdminSidebar from './components/AdminSidebar/AdminSidebar'; // Import the Sidebar component

const AdminDash = () => {
    return (
        <div className="dashboard-container">
            <AdminSidebar />
            <div className="main-content">
                {/* Your main dashboard content goes here */}
            </div>
        </div>
    );
}

export default AdminDash;
