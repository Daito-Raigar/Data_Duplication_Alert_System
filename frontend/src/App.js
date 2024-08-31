import React from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import LoginForm from './components/Login_Page/Login';
import SignupForm from './components/Signup_Page/Signup';
// import Forgot from './components/Forgot_Password/Forgot';
import Sidebar from './components/Side_bar/Sidebar';
import Dashboard from './components/Dash_board/Dashboard';
import Settings from './components/Bar/Settings';
import CollabWork from './components/Bar/CollabWork';
import Upgrade from './components/Bar/Upgrade';
import UserProfile from './components/Bar/Userprofile';
import './App.css';


const App = () => {
  return (
    <Router>
      <AppContent />
    </Router>
  );
};

const AppContent = () => {
  const location = useLocation();

  // Determine whether to show the sidebar
  const showSidebar = location.pathname !== '/' && location.pathname !== '/login' && location.pathname !== '/signup';

  return (
    <div style={{ display: 'flex', height:'auto' }}>
      {showSidebar && <Sidebar />}
        <Routes>
          <Route path="/" element={<SignupForm />} /> {/* Navigate to Signup page */}
          <Route path="/login" element={<LoginForm />} /> {/* Navigate to Login page */}
          <Route path="/signup" element={<SignupForm />} />
          {/* <Route path="/forgot" element={<Forgot />} /> Navigate to Forgot Password page */}
          <Route path="/dash" element={<Dashboard />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/collab-work" element={<CollabWork />} />
          <Route path="/upgrade" element={<Upgrade />} />
          <Route path="/profile" element={<UserProfile />} />
        </Routes>
      </div>
  );
};

export default App;
