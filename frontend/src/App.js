import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginForm from './components/Login_Page/Login';
import SignupForm from './components/Signup_Page/Signup';
import { Forgot } from './components/Forgot_Password/Forgot';
//import './App.css';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<SignupForm />} /> {/*navigate to Signup page */}
        <Route path='/login' element={<LoginForm />} /> {/*navigate to Login page */}
        <Route path='/signup' element={<SignupForm />} />
        <Route path='/forgot' element={<Forgot />} /> {/*navigate to Forgot Password page */}
      </Routes>
    </Router>
  );
};
export default App;