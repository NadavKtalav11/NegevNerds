import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SignUpCode.css';
import axios from 'axios';
import axiosInstance from '../../../utils/axiosInstance';


function SignUpCode() {
    const navigate = useNavigate(); // Create navigate object
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const [formData, setFormData] = useState({
        auth_code: '', // Form field for auth_code
    });
    const [message, setMessage] = useState('');

    // Handle form input changes
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value, // Update auth_code in formData
        });
        console.log('Input Changed:', name, value); // Log input changes for debugging
    };

    // Handle form submission and make HTTP POST request
    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevent form default submit behavior

        console.log('Form Data on Submit:', formData); // Log form data before submitting

        try {
            const response = await axiosInstance.post(`${API_BASE_URL}/api/register_authentication_part`, {
                auth_code: formData.auth_code,
                email: localStorage.getItem('email'),
                // Send auth_code from formData
            });

            setMessage('קוד תקין'); // Success message
            console.log(response.data); // Log response data
            navigate('/signupterms');
        } catch (error) {
            setMessage(error.response?.data?.message || 'קוד שגוי'); // Error message if failure
        }
    };

    return (
        <div className="welcome-page">
            <div className="background-logo">
                <div className="image-layer"></div> {/* Image layer */}
                <div className="content">
                    <h1 className="welcome-title">אימות דו-שלבי</h1>
                    {/* Registration form */}
                    <div className="login-container">
                        <p className="instruction">נא להזין את הקוד שקיבלת במייל:</p>
                        <form className="login-form" onSubmit={handleSubmit}>
                            <div className="code-input-group">
                                <input
                                    className="code-input-group input"
                                    type="text"
                                    name="auth_code" // Ensure name is correctly set to match formData
                                    maxLength="6"
                                    value={formData.auth_code} // Bind value to formData
                                    onChange={handleChange}
                                    required
                                />
                            </div>
                            <button type="submit" className="code-submit-button">
                                אישור
                            </button>
                        </form>
                        {/* Display message based on submission success or failure */}
                        {message && <p className="styles.message">{message}</p>}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default SignUpCode;
