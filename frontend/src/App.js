import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginForm from './components/Login_Page/Login';
import SignupForm from './components/Signup_Page/Signup';
import Dashboard from './components/Dashboard/Dashboard';
// import { Forgot } from './components/Forgot_Password/Forgot';
import WebSocketClient from './components/Websocket/websocket';
import Settings from './components/Bar/Settings';
import CollabWork from './components/Bar/CollabWork';
import Upgrade from './components/Bar/Upgrade';
import UserProfile from './components/Bar/Userprofile';
import Sidebar from './components/Side_bar/Sidebar';
//import './App.css';

const App = () => {
  return (
    <Router>
      <WebSocketClient />
      <Routes>
        <Route path='/' element={<SignupForm />} /> {/*navigate to Signup page */}
        <Route path='/login' element={<LoginForm />} /> {/*navigate to Login page */}
        <Route path='/signup' element={<SignupForm />} />
        <Route path='/dashboard' element={<Dashboard />} />
        {/* <Route path='/forgot' element={<Forgot />} /> navigate to Forgot Password page */}
      </Routes>
    </Router>
  );
};
export default App;