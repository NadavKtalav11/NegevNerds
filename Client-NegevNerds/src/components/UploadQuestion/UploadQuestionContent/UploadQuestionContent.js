// Course.js
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import Select from "react-select";
import Header from '../../Header/Header';
import Footer from '../../Footer/Footer';  // ייבוא הפוטר
import './UploadQuestionContent.css';
import axiosInstance from '../../../utils/axiosInstance';


function UploadQuestionContent() {
    const { courseId, examYear, examSemester, examDateSelection, questionNum } = useParams();  // מקבלים את שם הקורס מה-URL
    const [courseDetails, setCourseDetails] = useState(null);
    const [questionFile, setQuestionFile] = useState(null);
    const [answerFile, setAnswerFile] = useState(null);
    const [isAmerican, setAmerican] = useState(null);
    const [topics, setTopics] = useState([]);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [selectedTopics, setSelectedTopics] = useState([]);
    const navigate = useNavigate();  // יצירת אובייקט navigate
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const handleCancelClick = () => {
        navigate('/home');  // מנווט לעמוד ההרשמה
      };

    // const handleConfirmClick = () => {
    //     // call API for add question
    //     // if success - navigate to the new question page
    //     navigate(`/question/${courseId}/${examYear}/${examSemester}/${examDateSelection}/${questionNum}`);
    //   };

    const addAuthHeaders = (headers = {}) => {
        const token = localStorage.getItem('access_token');  // הוצאת ה-token מ-localStorage
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;  // הוספת ה-token להדר Authorization
        }
        return headers;
    };

    const handleConfirmClick = async () => {
        // Validate the inputs
        if (!questionFile) {
            alert("Please upload a question file.");
            return;
        }
        if (isAmerican === null) {
            alert("Please select a question type.");
            return;
        }
    
        const formData = new FormData();
        formData.append('course_id', courseId);
        formData.append('year', examYear);
        formData.append('semester', examSemester);
        formData.append('moed', examDateSelection);
        formData.append('question_number', questionNum);
        formData.append('is_american', isAmerican);
        formData.append('question_topics', JSON.stringify(selectedTopics.map(topic => topic.value)));
        formData.append('pdf_question', questionFile);
    
        if (answerFile) {
            formData.append('pdf_answer', answerFile);
        }
    
        try {
            setIsSubmitting(true);
            // Make the API call
            const response = await axiosInstance.post(`${API_BASE_URL}/api/course/add_question`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                }
            });
    
            // Handle success
            if (response.data.success) {
                alert("Question added successfully!");
                navigate(`/question/${courseId}/${examYear}/${examSemester}/${examDateSelection}/${questionNum}`);
            } else {
                // Handle failure
                alert(`Failed to add question: ${response.data.message}`);
            }
        } catch (error) {
            // Handle error
            console.error("Error adding question:", error);
            alert("An error occurred while adding the question.");
        }
        setIsSubmitting(false);
    };

    const handleTopicChange = (selected) => {
        setSelectedTopics(selected || []);
      };

    useEffect(() => {
    if (courseId) {
        axiosInstance.get(`${API_BASE_URL}/api/course/get_course/${courseId}`, {headers: addAuthHeaders()})
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

    
    
    useEffect(() => {
        axiosInstance.get(`${API_BASE_URL}/api/course/get_course_topics`, {
            params: { course_id: courseId },
            headers: addAuthHeaders()        
        })
        .then(response => {
            if (response.data.status == 'success') {
                setTopics(response.data.data); // עדכון ה-state עם הנושאים של הקורס
            } else {
                console.error('לא ניתן להוריד נושאים');
            }
        })
        .catch(error => {
            console.error('שגיאה בקריאת ה-API עבור נושאים:', error);
        });
    }, []); 

    if (!courseDetails) {
        return <div>Loading...</div>;
    }
    
    return (
        <div className="upload-question-content-page">
            <Header />
            <main className="content">
                <h1>העלאת שאלה חדשה</h1>
                <div className="details-container">
                    <div className="detail-item">
                        <strong>קורס</strong> {courseDetails.course_id} - {courseDetails.name}
                    </div>
                    <div className="detail-item">
                        <strong>שנה</strong> {examYear}
                    </div>
                    <div className="detail-item">
                        <strong>סמסטר</strong> {examSemester}
                    </div>
                    <div className="detail-item">
                        <strong>מועד</strong> {examDateSelection}
                    </div>
                    <div className="detail-item">
                        <strong>שאלה</strong> {questionNum}
                    </div>
                </div>
                <div className="question-content-form">
                    <div className="form-group">
                        <label className="label-question-content" htmlFor="name">שאלה:</label>
                        <div class="info-icon" title="העלה קובץ PDF או תמונה של השאלה כפי שמופיעה במבחן">i</div>
                        <input
                            className="question-content-field"
                            type="file"
                            accept=".pdf, .jpeg, .jpg, .png"
                            onChange={(e) => setQuestionFile(e.target.files[0])}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label className="label-question-content" htmlFor="name">פתרון רשמי:</label>
                        <div class="info-icon" title="במידה וקיים ברשותך פתרון רשמי לשאלה, העלה קובץ PDF או תמונה של פתרון זה">i</div>
                        <input
                            className="question-content-field"
                            type="file"
                            accept=".pdf, .jpeg, .jpg, .png"
                            onChange={(e) => setAnswerFile(e.target.files[0])}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label className="label-question-content" htmlFor="name">סוג השאלה:</label>
                        <div class="info-icon" title="בחר את סוג השאלה - אמריקאית או פתוחה">i</div>
                        <select
                            value={isAmerican === null ? '' : isAmerican ? 'אמריקאית' : 'פתוחה'}
                            onChange={(e) => {
                                const value = e.target.value;
                                if (value === '') {
                                    setAmerican(null); // אם בחרו אופציה ריקה, מאפסים ל-null
                                } else {
                                    setAmerican(value === 'אמריקאית'); // אם אמריקאית, true; אחרת false
                                }}
                            }
                            className="question-content-field"
                            required
                        >
                            <option value=""></option>
                            <option>אמריקאית</option>
                            <option>פתוחה</option>
                        </select>
                    </div>
                    <div className="form-group">
                        <label className="label-question-content" htmlFor="name">נושאי השאלה:</label>
                        <div class="info-icon" title="בחר את נושאי הקורס בהם עוסקת שאלה זו">i</div>
                        <Select
                            id="multi-select"
                            options={topics.map((topic) => ({ value: topic, label: topic }))} // המרה לפורמט מתאים
                            isMulti // מאפשר בחירה מרובה
                            value={selectedTopics}
                            onChange={handleTopicChange}
                            className="question-content-field"
                        />
                    </div>
                    <div className="question-button-row">
                        <button className="add-question-button" onClick={handleConfirmClick} disabled={isSubmitting}>
                            סיום
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

export default UploadQuestionContent;
