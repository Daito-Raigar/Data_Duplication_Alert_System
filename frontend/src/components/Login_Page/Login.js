import React , { useState }from 'react';
import './Login.css';
import { FaUser, FaLock, FaUnlock } from "react-icons/fa";
import { Link } from 'react-router-dom';

const LoginForm = () => {
    const [passView, setView] = useState(false);

    const toggle = () => {
        setView(!passView);
      };

    return(
        <div className='wrapper2'>
            <form action=''>
                <h1>Login</h1>
                <div className='input-box'>
                    <input type='text' placeholder='Username' required />
                    <FaUser className='icon'/>
                </div>
                <div className='input-box'>
                    <input type={passView ? 'text' : 'password'} placeholder='Password' required />
                    <span onClick={toggle}>{passView ? <FaUnlock className='icon' /> : <FaLock className='icon' />}</span>
                    
                </div>

                {/* <div className='remember-forgot'>
                    <label><input type='checkbox' />Remember me</label>
                    <Link to='/forgot'>Forgot password?</Link>
                </div> */}

                <button type='submit'>Login</button>

                <div className='register-link'>
                    <p>Don't have an account? <Link to='/signup'>Register</Link></p>
                </div>
            </form>
        </div>
    );
};

export default LoginForm;