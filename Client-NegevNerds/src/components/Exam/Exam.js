// Exam.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { faStar } from '@fortawesome/free-solid-svg-icons'; // כוכב מלא
import { faStar as faStarRegular } from '@fortawesome/free-regular-svg-icons'; // כוכב ריק
import { faEye } from '@fortawesome/free-solid-svg-icons'; // עין
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { BsEmojiSmile } from "react-icons/bs";
import { FaRegCommentAlt, FaCommentAlt } from 'react-icons/fa';
import { BiDownArrow, BiSolidUpArrow } from "react-icons/bi";
import Header from '../Header/Header';
import Footer from '../Footer/Footer';  // ייבוא הפוטר
import './Exam.css';
import axiosInstance from '../../utils/axiosInstance';

import { useNavigate } from "react-router-dom";

function Exam() {
    const [searchResults, setSearchResults] = useState([]); // אם אין תוצאות, הוא יהיה מערך ריק
    const [allQuestions, setAllQuestions] = useState([]);  // התחלה של מערך ריק
    const [isModalOpen, setIsModalOpen] = useState(false); // New state for modal visibility
    const [token, setToken] = useState('');  // מזהה היוזר
    const [examFile, setExamFile] = useState(null);
    const [examExist, setExamExist] = useState(false);
    const { courseId, examYear, examSemester, examDateSelection } = useParams();  // מקבלים את שם הקורס מה-URL
    const [courseDetails, setCourseDetails] = useState(null);
    const navigate = useNavigate();
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;


    const handleFileChange = (e) => setExamFile(e.target.files[0]);

    const addAuthHeaders = (headers = {}) => {
        const token = localStorage.getItem('access_token');  // הוצאת ה-token מ-localStorage
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;  // הוספת ה-token להדר Authorization
        }
        return headers;
    };
    
    const handleFileUpload = async () => {
        if (!examFile) {
            alert("Please select a file to upload.");
            return;
        }
    
        const formData = new FormData();
        formData.append('course_id', courseId);
        formData.append('year', examYear);
        formData.append('semester', examSemester);
        formData.append('moed', examDateSelection);
        formData.append('pdf_exam', examFile); // Adjust the key if needed for your backend API
    
        try {
            const response = await axiosInstance.post(`${API_BASE_URL}/api/course/uploadFullExamPdf`, formData, {
                headers: { 'Content-Type': 'multipart/form-data', ...addAuthHeaders() } // Include the Authorization header,
            });
    
            if (response.data.success) {
                alert("File uploaded successfully!");
                closeModal();
                window.location.reload();
            } else {
                alert(`Failed to upload file: ${response.data.message}`);
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            alert("An error occurred while uploading the file.");
        }
    };

    const navigateToQuestionPage = (question_number) => {
        navigate(`/question/${courseId}/${examYear}/${examSemester}/${examDateSelection}/${question_number}`);
    };

    useEffect(() => {
        const storedToken = localStorage.getItem('access_token');
        setToken(storedToken);
        const fetchData = async () => {
            if (courseId) {
                try {
                    // טעינת פרטי הקורס
                    const courseResponse = await axiosInstance.get(`${API_BASE_URL}/api/course/get_course/${courseId}`, {
                        headers: addAuthHeaders()  
                    });
                    if (courseResponse.data && courseResponse.data.status === 'success') {
                        setCourseDetails(courseResponse.data.data);
                    }

                    // טעינת קובץ המבחן האם קיים
                    const response = await axiosInstance.post(`${API_BASE_URL}/api/checkExamFullPdf`, 
                        {
                            course_id: courseId,
                            year: examYear,
                            semester: examSemester,
                            moed: examDateSelection,  // העברת הנתונים בגוף הבקשה, לא ב-params
                        }, 
                        {
                            headers: addAuthHeaders()  // הוספת הכותרת המתאימה
                        } 
                    );
                    if (response.data.success) {
                        setExamExist(response.data.has_link)
                    } 

                    // טעינת כל השאלות של המבחן
                    const questionsResponse = await axiosInstance.post(`${API_BASE_URL}/api/course/search_question_by_specifics`, 
                        {
                            course_id: courseId,  // העברת הנתונים בגוף הבקשה, לא ב-params
                        }, 
                        {
                            headers: addAuthHeaders()  // הוספת הכותרת המתאימה
                        }
                    );
                    let parsedResponse;
                    if (typeof questionsResponse.data.data === 'string') {
                        parsedResponse = JSON.parse(questionsResponse.data.data); // המרת המחרוזת לאובייקט

                    } else {
                        parsedResponse = questionsResponse.data.data; // אם כבר אובייקט, השתמש בו
                    }
    
                    if (parsedResponse.status === 'success' && parsedResponse.data.length > 0) {
                        const filteredQuestions = parsedResponse.data.filter(
                            (question) =>
                                String(question.year) === String(examYear) &&
                                String(question.semester) === String(examSemester) &&
                                String(question.moed) === String(examDateSelection)
                        );
                        setAllQuestions(filteredQuestions);  // עדכון תוצאות החיפוש אם הם מערך
                    } else {
                        setAllQuestions([]);  // אם לא, הפוך את allQuestions למערך ריק
                    }
    
                } catch (error) {
                    console.error('Error fetching data:', error);
                    setAllQuestions([]);  // לנקות אם יש שגיאה
                }
            }
    
        };
    
        fetchData();
    }, []);

    const sortedQuestions = [...allQuestions].sort((a, b) => {
        // מיון לפי שנה
        if (a.question_number !== b.question_number) {
            return a.question_number - b.question_number;
        }
    });

    const handleSort = (column) => {
        // מיון תוצאות החיפוש לפי העמודה
        const sortedResults = [...searchResults].sort((a, b) => {
            if (a[column] < b[column]) return -1;
            if (a[column] > b[column]) return 1;
            return 0;
        });
        setSearchResults(sortedResults);
    };

    const downloadExamPdf = async () => {
        try {
            const response = await axiosInstance.post(
                `${API_BASE_URL}/api/course/downloadExamPdf`,
                {
                    course_id: courseId,
                    year: examYear,
                    semester: examSemester,
                    moed: examDateSelection,
                },
                {
                    headers: addAuthHeaders()  
                },
                {
                    responseType: 'blob', // Expect binary data
                }
            );
    
            if (response.headers['content-type'] === 'application/json') {
                // Handle the case where the response is JSON (no file link exists)
                const reader = new FileReader();
                reader.onload = () => {
                    const result = JSON.parse(reader.result);
                    if (!result.has_link) {
                        alert(result.message);
                    }
                };
                reader.readAsText(response.data);
            } else {
                // Handle the case where the response is a file
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
    
                // Use the expected file name
                const fileName = `${courseId}_${examYear}_${examSemester}_${examDateSelection}.pdf`;
                link.setAttribute('download', fileName);
    
                document.body.appendChild(link);
                link.click();
                link.parentNode.removeChild(link);
            }
        } catch (error) {
            if (error.response && error.response.data.message) {
                alert(error.response.data.message);
            } else {
                console.error('Error downloading exam PDF:', error);
                alert('An error occurred while trying to download the exam.');
            }
        }
    };
    
    const openModal = () => setIsModalOpen(true); // Open modal
    const closeModal = () => {
        setIsModalOpen(false);
        setExamFile(null);
    };
      
    const adddExamPdf = async () => {
        try {
            const response = await axiosInstance.post(`${API_BASE_URL}/api/checkExamFullPdf`,
                {
                    course_id: courseId,
                    year: examYear,
                    semester: examSemester,
                    moed: examDateSelection,  // העברת הנתונים בגוף הבקשה, לא ב-params
                }, 
                {
                    headers: addAuthHeaders()  // הוספת הכותרת המתאימה
                } 
            );

            if (response.data.success) {
                if (response.data.has_link) {
                    alert("המבחן כבר קיים במערכת. את/ה מוזמנ/ת להוריד אותו");
                } else {
                    openModal();
                }
            } else {
                alert(`Failed to check the exam: ${response.data.message || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Error checking exam:', error);
            alert('An error occurred while checking the exam.');
        }
    };

    if (!courseDetails) {
        return <div>Loading...</div>;
    }
    return (
        <div className="upload-question-content-page">
            <Header />
            <main className="content">
                <h1>דף מבחן</h1>
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
                </div>
                <div className="tabs-container">
                   {examExist ? 
                    (<button
                        className="tab download-tab"
                        onClick={downloadExamPdf}
                    >
                        הורדת המבחן המלא
                    </button>):
                    (<button
                        className="tab download-tab"
                        onClick={adddExamPdf}
                    >
                        העלאת המבחן המלא
                    </button>)}
                    <button
                        className="tab download-tab"
                    >
                        העלאת שאלה חדשה
                    </button>
                    <button
                        className='tab download-tab'
                        onClick={() => navigate(`/course/${courseId}`)}
                        title="לדף הקורס"
                    >
                        <i className="fas fa-arrow-left"></i> 
                    </button>
                </div>
                <div className="updates-container">
                    <h3>שאלות במבחן זה</h3>
                    <ul className="results-list">
                            {sortedQuestions && Array.isArray(sortedQuestions) && sortedQuestions.length > 0 ? (
                                sortedQuestions.map((result) => (
                                    <li key={result.question_id} className="result-item">
                                        <a href={`/question/${courseId}/${result.year}/${result.semester}/${result.moed}/${result.question_number}`} className="result-link">
                                            <span>{courseDetails.name} / {result.year} / {result.semester} / מועד {result.moed} / שאלה {result.question_number}</span>
                                        </a>
                                    </li>
                                ))
                            ) : (
                                <p>לא נמצאו שאלות</p>
                            )}
                        </ul>
                    {/* <table className="search-results-table">
                        <thead>
                            <tr>
                                <th onClick={() => handleSort('year')}>שנה</th>
                                <th onClick={() => handleSort('semester')}>סמסטר</th>
                                <th onClick={() => handleSort('moed')}>מועד</th>
                                <th onClick={() => handleSort('question_number')}>מספר שאלה</th>
                                <th>צפייה</th>
                            </tr>
                        </thead>
                        <tbody>
                            {allQuestions && Array.isArray(allQuestions) && allQuestions.length > 0 ? (
                                allQuestions.map(result => (
                                    <tr key={result.question_id}>
                                        <td>{result.year}</td>
                                        <td>{result.semester}</td>
                                        <td>{result.moed}</td>
                                        <td>{result.question_number}</td>
                                        <td>
                                            <button onClick={() => navigateToQuestionPage(result.question_number)}>
                                                <FontAwesomeIcon icon={faEye} />
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="5">לא נמצאו שאלות</td>
                                </tr>
                            )}
                        </tbody>
                    </table> */}
                </div>
                {isModalOpen && (
                        <div className="modal-overlay">
                            <div className="modal-content">
                                <button className="modal-close" onClick={closeModal}>X</button>
                                <h2>Upload Exam File</h2>
                                <input type="file" onChange={handleFileChange} />
                                <div className="modal-actions">
                                    <button className="upload-btn" onClick={handleFileUpload}>Upload</button>
                                    <button className="cancel-btn" onClick={closeModal}>Cancel</button>
                                </div>
                            </div>
                        </div>
                    )}
            </main>
            <Footer />
        </div>
    );
}    
export default Exam;

