import React , { useState }from 'react';
import './Signup.css';
import { FaUser, FaLock, FaUnlock, FaMobile } from "react-icons/fa";
import { MdAlternateEmail } from "react-icons/md";
import { Link } from 'react-router-dom';

const SignupForm = () => {
    const [passView, setView] = useState(false); //Used to see password
    const [password, setPass] = useState(''); //Contains password value for checking
    const [confirmPass, setConfPass] = useState(''); //Contains confirm password value for checking
    const [match, setMatch] = useState(true); //Used to check password is correctly being entered
    const [phone, setPho] = useState(''); //Contains phone no value for checking
    const [Phoval, setPhoVal] = useState(true); //Used to check for valid mobile no
    //const [phoneTouch, setPhoTouch] = useState(false); //Used to check field is entered or not
    const [email, setEmail] = useState(''); //Contains email value for checking
    const [mailVal, setmail] = useState(true); // Used to check 
    const [emailTouch, setEmailTouch] = useState(false); // Track if the email input has been touched

    const toggle = () => {
        setView(!passView);
    };

    const handlePass = (e) => {
        setPass(e.target.value);
    };
    
    const handleConfirmPass = (e) => {
        setConfPass(e.target.value);
        setMatch(e.target.value === password);
    };
    
    const handlePhone = (e) => {
        const input = (e.target.value);
        if (/^\d{0,10}$/.test(input)) {
            setPho(input);
            setPhoVal(phone.length === 10)
        }
    };

    // const PhoneBlur = () => {
    //     setPhoTouch(true);
    //     setPhoVal(phone.length === 10)
    //   };

    const handleEmail = (e) => {
        setEmail(e.target.value);
    };

    const EmailBlur = () => {
        setEmailTouch(true);
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        setmail(emailRegex.test(email));
    };

    return(
        <div className='wrapper1'>
            <form action=''>
                <h1>Signup</h1>
                <div className='input-box'>
                    <input type='text' placeholder='Username' required />
                    <FaUser className='icon'/>
                </div>

                <div className={`input-box ${mailVal ? '' : 'invalid'}`}>
                    <input type='text' placeholder='Email ID' value={email} onChange={handleEmail} onBlur={EmailBlur} required/>
                    <MdAlternateEmail className='icon' />
                    { emailTouch && !mailVal && <p style={{ color: 'red' }}>Please enter a valid email address</p>}
                </div>
                
                
                <div className='input-box'>
                    <input type='text' placeholder='Phone No' value={phone} onChange={handlePhone} required />
                    <FaMobile className='icon'/>
                    { !Phoval && (<p style={{ color: 'red' }}>Phone number must be exactly 10 digits.</p>)}
                </div>

                <div className='input-box'>
                    <input type={passView ? 'text' : 'password'} placeholder='Password' value={password} onChange={handlePass} required />
                    <span onClick={toggle}>{passView ? <FaUnlock className='icon' /> : <FaLock className='icon' />}</span>
                </div>

                <div className='input-box'>
                    <input type={passView ? 'text' : 'password'} placeholder='Confirm Password' value={confirmPass} onChange={handleConfirmPass} required />
                    <span onClick={toggle}>{passView ? <FaUnlock className='icon' /> : <FaLock className='icon' />}</span>
                    {!match && <p style={{ color: 'red' }}>Passwords do not match</p>}
                </div>
                

                <button type='submit'>Signup</button>

                <div className='register-link'>
                    <p>Already have an account? <Link to='/login'>Login</Link></p>
                </div>
            </form>
        </div>
  );
};

export default SignupForm;