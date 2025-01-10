import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SignUpTerms.css';
import axios from 'axios'; // Import Axios for HTTP requests
import axiosInstance from '../../../utils/axiosInstance';


function SignUpTerms() {
    // Static terms of use content
    const termsOfUseContent = `
        ברוכים הבאים לשירות NegevNerds, אנא קרא בעיון את תנאי השימוש להלן לפני השימוש בשירות:
        1. השימוש בשירות מותנה בקבלת תנאי השימוש המפורטים להלן.
        2. חל איסור מוחלט להשתמש בשירות לצרכים בלתי חוקיים או לכל מטרה שנוגדת את החוק.
        3. כל המידע והנתונים המוזנים על ידך לשירות יישמרו בהתאם למדיניות הפרטיות שלנו.
        4. השירות ניתן כפי שהוא (AS IS) ואנו לא נישא באחריות לכל נזק שייגרם כתוצאה מהשימוש בו.
        5. אנו שומרים לעצמנו את הזכות לשנות או לעדכן את תנאי השימוש בכל עת, מבלי להודיע מראש.
        6. חל איסור מוחלט להעליב, לפגוע או להשתמש בשפה פוגענית כלפי משתמשים אחרים באתר, לרבות בדיווחים, בתגובות ובפורומים.
        דוגמאות למילים אסורות:
        - קללות: מטומטם, דפוק, זין, אפס, חרא, בן זונה
        - ביטויים פוגעניים: לך תמות, אדיוט, מכוער, תסתום את הפה
        - כל ביטוי נוסף שעשוי לפגוע בכבודו או בתחושותיו של משתמש אחר.
        על ידי לחיצה על הכפתור מטה, אתה מאשר כי קראת, הבנת והסכמת לכל תנאי השימוש, כולל סעיף האוסר על שימוש בשפה פוגענית.
        תודה על השימוש בשירות שלנו!
    `;

    const navigate = useNavigate();  // Create navigate object
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const [message, setMessage] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);  // Track submission state

    // Handle form submission and make HTTP POST request
    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);  // Disable submit button during submission

        try {
            const response = await axiosInstance.post(`${API_BASE_URL}/api/register_termOfUse_part`, {
                email: localStorage.getItem('email'),
                password: localStorage.getItem('password'),
                first_name: localStorage.getItem('first_name'),
                last_name: localStorage.getItem('last_name'),

            });
            if (response.data.success) {
                // Save user_id to localStorage
                const userId = response.data.user_id;
                localStorage.setItem('access_token', response.data.access_token); // שמירת הטוקן ב-localStorage

                console.log('User ID:', userId);
                //localStorage.setItem('user_id', userId);
                localStorage.removeItem('password');


            }

            setMessage('ההרשמה בוצעה בהצלחה!');  // Success message
            console.log(response.data);  // Log the response if needed
            navigate('/home');  // Navigate to the home page
        } catch (error) {
            setMessage(error.response?.data?.message || 'ההרשמה נכשלה. בדוק את הפרטים שלך.');
        }

        setIsSubmitting(false);  // Re-enable submit button after submission
    };

    return (
        <div className="welcome-page">
            <div className="background-logo">
                <div className="image-layer"></div> {/* Image layer */}
                <div className="content">
                    <h1 className="welcome-title">תקנון האתר</h1>
                    <div className="terms-container">
                        <form className="login-form" onSubmit={handleSubmit}>
                            <p className="termsofuse-text">
                                {termsOfUseContent}
                            </p>
                            <button
                                type="submit"
                                className="submit-button"
                                disabled={isSubmitting}  // Disable the button during submission
                            >
                                {isSubmitting ? 'שליחה...' : 'אני מסכים לתנאי השימוש'}
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default SignUpTerms;