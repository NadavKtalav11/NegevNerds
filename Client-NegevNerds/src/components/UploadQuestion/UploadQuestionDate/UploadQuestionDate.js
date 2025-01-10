// Course.js
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import Header from '../../Header/Header';
import Footer from '../../Footer/Footer';  // ייבוא הפוטר
import './UploadQuestionDate.css';
import axiosInstance from '../../../utils/axiosInstance';


function UploadQuestionDate() {
    const { courseId } = useParams();  // מקבלים את שם הקורס מה-URL
    const navigate = useNavigate();  // יצירת אובייקט navigate
    const semesters = ['סתיו', 'אביב', 'קיץ'];
    const examDates = ['א', 'ב', 'ג', 'ד'];
    const [courseDetails, setCourseDetails] = useState(null);
    const [examYear, setExamYear] = useState(''); // שנה של המבחן
    const [examSemester, setExamSemester] = useState(''); // סמסטר של המבחן
    const [examDateSelection, setExamDateSelection] = useState(''); // מועד של המבחן
    const [questionNum, setQuestionNum] = useState(''); // מספר שאלה
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const addAuthHeaders = () => {
        const token = localStorage.getItem('access_token'); // או מקורות אחרים לשמירת ה-token
        return {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json', // אם יש צורך
        };
    };
    
    useEffect(() => {
        if (courseId) {
            axiosInstance.get(`${API_BASE_URL}/api/course/get_course/${courseId}`, { headers: addAuthHeaders() })
                .then(response => {
                    console.log('Response received:', response);
                    
                    if (response.data && response.data.status === 'success') {
                        console.log('Course data:', response.data.data); // הדפס את המידע שהתקבל
                        setCourseDetails(response.data.data);  // עדכון הסטייט עם פרטי הקורס
                    } else {
                        console.error('Response does not contain valid course data', response.data);
                    }
                })
                .catch(error => {
                    console.error('Error fetching course details:', error);
                });
        }
    }, [courseId]); 

    if (!courseDetails) {
        return <div>Loading...</div>;
    }
    
    const handleConfirmClick = () => {
        if (examYear && examSemester && examDateSelection && questionNum) {
            if(examYear < 1960){
                alert("שנה לא תקינה");
            }
            else if(questionNum < 1){
                alert("מספר שאלה לא תקין");
            }
            else{
                console.log("חיפוש לפי מועד עם פרמטרים: ", { courseId, examYear, examSemester, examDateSelection, questionNum });
                
                // קריאה ל-API לחיפוש לפי מועד
                axiosInstance.post(`${API_BASE_URL}/api/course/search_question_by_specifics`, {
                    course_id: courseId,
                    year: examYear,
                    semester: examSemester,
                    moed: examDateSelection,
                    question_number: questionNum
                }, {
                    headers: addAuthHeaders()
                })
                .then(response => {
                    const parsedResponse = JSON.parse(response.data.data);  // המרת המחרוזת לאובייקט    
                    console.log(parsedResponse.status)
                    if (parsedResponse.status==="success" && parsedResponse.data.length == 1) {
                        const userChoice = window.confirm(
                            "שאלה זו קיימת במאגר. האם ברצונך לעבור לדף השאלה?"
                        );
                        if (userChoice) {
                            navigate(`/question/${courseId}/${examYear}/${examSemester}/${examDateSelection}/${questionNum}`);
                        } 
                    } else {
                        navigate(`/upload-question-content/${courseId}/${examYear}/${examSemester}/${examDateSelection}/${questionNum}`);
                    }
                })
                .catch(error => {
                    console.error('שגיאה בחיפוש לפי מועד:', error);
                    alert("אירעה שגיאה בחיפוש לפי מועד");
                });
            }
          } else {
            // Optionally, you can alert the user or show a message if no course is selected
            alert("אנא מלא את כל השדות.");
          }
    };
    
    const handleCancelClick = () => {
        navigate('/home');  // מנווט לעמוד ההרשמה
      };

    return (
        <div className="upload-question-date-page">
            <Header />
            <main className="content">
                <h1>העלאת שאלה חדשה</h1>
                <div className="question-content-form">
                    <div className="form-group">
                        <label className="label-question-content" htmlFor="name">מספר קורס:</label>
                        <input
                            type="text" 
                            disabled 
                            value={courseId}
                            className="question-date-field"
                            required
                        >
                        </input>
                    </div>
                    <div className="form-group">
                        <label className="label-question-content" htmlFor="name">שם קורס:</label>
                        <input
                            type="text" 
                            disabled 
                            value={courseDetails.name}
                            className="question-date-field"
                            required
                        >
                        </input>
                    </div>
                    <div className="form-group">
                        <label className="label-question-content" htmlFor="name">שנה:</label>
                        <input
                            type="number"
                            value={examYear}
                            onChange={(e) => {setExamYear(e.target.value)}}
                            className="question-date-field"
                            min="1960"
                        />
                    </div>
                    <div className="form-group">
                        <label className="label-question-content" htmlFor="name">סמסטר:</label>
                        <select
                            value={examSemester}
                            onChange={(e) => setExamSemester(e.target.value)}
                            className="question-date-field"
                        >
                            <option value=""></option>
                            {semesters.map((semesterOption, index) => (
                                <option key={index} value={semesterOption}>
                                    {semesterOption}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="form-group">
                        <label className="label-question-content" htmlFor="name">מועד:</label>
                        <select
                            value={examDateSelection}
                            onChange={(e) => setExamDateSelection(e.target.value)}
                            className="question-date-field"
                        >
                            <option value=""></option>
                            {examDates.map((dateOption, index) => (
                                <option key={index} value={dateOption}>
                                    {dateOption}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="form-group">
                        <label className="label-question-content" htmlFor="name">מספר שאלה:</label>
                        <input
                            type="number"
                            value={questionNum}
                            onChange={(e) => setQuestionNum(e.target.value)}
                            className="question-date-field"
                            min="1"
                        />
                    </div>
                    <div className="question-button-row">
                        <button className="add-question-button" onClick={handleConfirmClick}>
                            אישור
                        </button>
                        <button className="add-question-button" onClick={handleCancelClick}>
                            ביטול
                        </button>
                    </div>
                </div>
                
            </main>
            <Footer />
        </div>
    );
}

export default UploadQuestionDate;