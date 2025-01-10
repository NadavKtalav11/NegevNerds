import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Home.css';
import Header from '../Header/Header';
import Footer from '../Footer/Footer';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../../utils/axiosInstance';

function Home() {
    const [courses, setCourses] = useState([]);  // קורסים כלליים
    const [userCourses, setUserCourses] = useState([]);  // קורסים של היוזר הספציפי    const [userId, setUserId] = useState(''); // כאן נשמור את ה-user ID
    const [token, setToken] = useState('');  // מזהה היוזר
    const [searchType, setSearchType] = useState('topic'); 
    const [selectedCourse, setSelectedCourse] = useState('');
    const [courseResults, setCourseResults] = useState('');
    const [courseForQuestion, setcourseForQuestion] = useState('');
    const [topics, setTopics] = useState([]);
    const [courseId, setCourseId] = useState('');

    const [selectedTopic, setSelectedTopic] = useState('');
    const [searchText, setSearchText] = useState(''); // שינוי שם ל-searchText

    const [examYear, setExamYear] = useState(''); // שינוי שם ל-examYear
    const [examSemester, setExamSemester] = useState(''); // שינוי שם ל-examSemester
    const [examDateSelection, setExamDateSelection] = useState(''); // שינוי שם ל-examDateSelection
    const [questionNum, setQuestionNum] = useState(''); // שינוי שם ל-questionNum

    const semesters = ['סתיו', 'אביב', 'קיץ'];
    const examDates = ['א', 'ב', 'ג', 'ד'];
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;


    const [isQuestionModalOpen, setIsQuestionModalOpen] = useState(false); // State לשליטה בפופ-אפ
    const openQuestionModal = () => setIsQuestionModalOpen(true);  // פונקציה לפתיחת הפופ-אפ
    const closeQuestionModal = () => setIsQuestionModalOpen(false); // פונקציה לסגירת הפופ-אפ

    const [isCourseNotFoundModalOpen, setIsCourseNotFoundModalOpen] = useState(false); // State לשליטה במודל פתיחת קורס חדש

    const [searchResults, setSearchResults] = useState([]); // אם אין תוצאות, הוא יהיה מערך ריק

    const addAuthHeaders = (headers = {}) => {
        const token = localStorage.getItem('access_token');  // הוצאת ה-token מ-localStorage
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;  // הוספת ה-token להדר Authorization
        }
        return headers;
    };

    const courseIdToNameMap = {};
    courses.forEach((course) => {
        courseIdToNameMap[course.course_id] = course.name;
    });
    
    useEffect(() => {
        const storedToken = localStorage.getItem('access_token');
        if (storedToken) {
            setToken(storedToken);
        }
    }, []);
    
    useEffect(() => {
        // API call to fetch all courses
        const token = localStorage.getItem('access_token');
        if (token) {
            console.log("Sending request with token get all courses:", token);
            axiosInstance.get(`${API_BASE_URL}/api/course/get_all_courses`, {
                headers: addAuthHeaders()
                })
                .then(response => {
                    // Set the courses state with the data array from the response
                    console.log("Response received get all courses:", response);  // הדפסה של התשובה שהתקבלה

                    setCourses(response.data.data);
                })
                .catch(error => {
                    console.error("שגיאה בגישה לכל הקורסים", error);
                });
        }
    }, []);// תבצע קריאה אחת בלבד כשקומפוננטה נטענת

    // קריאה לקבלת הנושאים של קורס
    useEffect(() => {
        if (selectedCourse) {

            axiosInstance.get(`${API_BASE_URL}/api/course/get_course_topics`, {
                params: { course_id: selectedCourse },
                headers: addAuthHeaders()
            })
            .then(response => {
                if (response.data.status === 'success') {
                    setTopics(response.data.data); // עדכון ה-state עם הנושאים של הקורס
                } else {
                    console.error('לא ניתן להוריד נושאים');
                }
            })
            .catch(error => {
                console.error('שגיאה בקריאת ה-API עבור נושאים:', error);
            });
        }
    }, [selectedCourse]); // הפעל מחדש את הקריאה כל פעם שהקורס משתנה

    useEffect(() => {
        // בצע קריאה ל-API כדי להשיג את הקורסים של המשתמש
        if (token) {
          axiosInstance.get(`${API_BASE_URL}/api/get_user_courses`, {
            headers: addAuthHeaders()
          })
          .then(response => {
            console.log('API Response:', response);
            if (response.data.success) {
              setUserCourses(response.data.courses); // עדכון הסטייט עם המערך של הקורסים
            } else {
              console.error('Failed to fetch user courses');
            }
          })
          .catch(error => {
            console.error('Error fetching user courses:', error);
          });
        }
      }, [token]);


    const navigate = useNavigate();

    const handleSearchTypeChange = (criteria) => {
        setSearchType(criteria);
    };

    const handleCourseSelection = (e) => {
        setSelectedCourse(e.target.value);
    };

    const getCourseName = (course_id) => {
        const course = courses.find(course => course.course_id === course_id);
        return course ? course.name : null; // מחזיר את שם הקורס או null אם לא נמצא
    }

    const handleCourseSelectionForQuestion = (e) => {
        setcourseForQuestion(e.target.value);
    };

    // const handleQuestionClick = (year, semester, moed, question_number) => {
    //     navigate(`/question/${selectedCourse}/${year}/${semester}/${moed}/${question_number}`);  // עובר לדף השאלה עם מזהה השאלה
    // };

    const handleSearch = () => {
        setSearchResults([])
        if (searchType === 'topic') {
            console.log("חיפוש לפי נושא עם פרמטרים: ", { selectedCourse, selectedTopic});
            // במקרה של חיפוש לפי נושא, תוכל להוסיף את קריאת ה-API המתאימה כאן
        } else if (searchType === 'date') {
            console.log("חיפוש לפי מועד עם פרמטרים: ", { selectedCourse, examYear, examSemester, examDateSelection, questionNum });
    
            // קריאה ל-API לחיפוש לפי מועד
            axiosInstance.post(`${API_BASE_URL}/api/course/search_question_by_specifics`, {
                course_id: selectedCourse,
                year: examYear || undefined,
                semester: examSemester || undefined,
                moed: examDateSelection || undefined,
                question_number: questionNum || undefined

            }, {
                headers: addAuthHeaders()
            })
            .then(response => {
                const parsedResponse = JSON.parse(response.data.data);  // המרת המחרוזת לאובייקט    
                if (parsedResponse.status === "success" && parsedResponse.data.length > 0) {
                    setSearchResults(parsedResponse.data);  // עדכון תוצאות החיפוש
                } else {
                    setSearchResults([]); // אם אין תוצאות, לנקות את ה-state
                }
            })
            .catch(error => {
                console.error('שגיאה בחיפוש לפי מועד:', error);
                setSearchResults([]); // אם קרתה שגיאה, לנקות את ה-state
                alert("אירעה שגיאה בחיפוש לפי מועד");
            });
        } else if (searchType === 'text') {
            console.log("חיפוש לפי טקסט עם פרמטרים: ", { selectedCourse, searchText });
    
            // קריאה ל-API לחיפוש לפי טקסט
            axiosInstance.post(`${API_BASE_URL}/api/course/search_questions_by_text`, {
                text: searchText,
                course_id: selectedCourse || undefined},
            {headers: addAuthHeaders()})
            .then(response => {
                const parsedResponse = JSON.parse(response.data.data);  // המרת המחרוזת לאובייקט    
                    // אם התוצאה היא לא מערך, נהפוך אותה למערך
                    console.log('API Response:', parsedResponse);
                    if (parsedResponse.status === "success" && parsedResponse.message.length > 0) {
                        console.log('API22 Response:', parsedResponse.message);
                        setSearchResults(parsedResponse.message);  // עדכון תוצאות החיפוש
                } else {
                    setSearchResults([]); // אם אין תוצאות, לנקות את ה-state
                }
            })
            .catch(error => {
                console.error('שגיאה בחיפוש לפי טקסט:', error);
                setSearchResults([]); // אם קרתה שגיאה, לנקות את ה-state
                alert("אירעה שגיאה בחיפוש לפי טקסט");
            });
        }
        setCourseResults(selectedCourse)
    };
    
    const navigateToUploadQuestion = () => {
        if (courseForQuestion) {
            // Navigate only if courseForQuestion has a valid value
            navigate(`/upload-question-date/${courseForQuestion}`);
          } else {
            // Optionally, you can alert the user or show a message if no course is selected
            alert("אנא בחר קורס לפני שתמשיך.");
          }
    };

    const navigateToAddExam = () => {
        navigate('/addexam');
    };

    const handleCourseSearch = (courseId) => {
        console.log("Searching for course with courseId:", courseId);
        
        if (courseId) {
            // מחפש את הקורס לפי ה-ID בתוך המערך של הקורסים
            const course = courses.find(course => course.course_id === courseId);
            if (course) {
                axiosInstance.get(`${API_BASE_URL}/api/course/get_course/${courseId}`, {
                    headers: addAuthHeaders()
                })
                    .then(response => {
                        console.log('Course data:', response.data);
                        navigate(`/course/${courseId}`); // אם הקורס נמצא, מעביר לדף הקורס
                    })
                    .catch(error => {
                        console.error('Error fetching course details:', error);
                    });
            } else {
                openCourseNotFoundModal(); // אם הקורס לא נמצא
            }
        } else {
            console.error('Course ID is missing');
        }
    };
    

    const openCourseNotFoundModal = () => {
        setIsCourseNotFoundModalOpen(true);
    };

    const closeCourseNotFoundModal = () => {
        setIsCourseNotFoundModalOpen(false);
    };

    const navigateToAddNewCourse = () => {
        navigate('/opencourse'); // ניווט לדף "פתיחת קורס חדש"
    };

    return (
        <div className="home-page">
            <Header />
            <main className="content">
            <h1>דף הבית</h1>
            <div className="tabs-container">
                <button
                    className={`tab ${searchType === 'topic' ? 'active' : ''}`}
                    onClick={() => handleSearchTypeChange('topic')}
                >
                    חיפוש לפי נושא
                </button>
                <button
                    className={`tab ${searchType === 'date' ? 'active' : ''}`}
                    onClick={() => handleSearchTypeChange('date')}
                >
                    חיפוש לפי מועד
                </button>
                <button
                    className={`tab ${searchType === 'text' ? 'active' : ''}`}
                    onClick={() => handleSearchTypeChange('text')}
                >
                    חיפוש לפי טקסט
                </button>
            </div>

                <div className="search-container">
                    {searchType === 'topic' && (
                        <div className="topic-search">
                            <select
                                value={selectedCourse}
                                onChange={handleCourseSelection}
                                className="search-input-course"
                            >
                                <option value="">בחר קורס</option>
                                {courses.map((course) => (
                                    <option key={course.course_id} value={course.course_id}>
                                        {course.name}
                                    </option>
                                ))}
                            </select>

                            <select
                                value={selectedTopic}
                                onChange={(e) => setSelectedTopic(e.target.value)}
                                className="search-input-topic"
                                disabled={!selectedCourse}
                            >
                                <option value="">בחר נושא</option>
                                {selectedCourse && topics.map((topic, index) => (
                                    <option key={index} value={topic}>
                                        {topic}
                                    </option>
                                ))}
                            </select>
                        </div>
                    )}

                    {searchType === 'text' && (
                        <div className="text-search">
                            <select
                                value={selectedCourse}
                                onChange={handleCourseSelection}
                                className="search-input-course"
                            >
                                <option value="">בחר קורס</option>
                                {courses.map((course) => (
                                    <option key={course.course_id} value={course.course_id}>
                                        {course.name}
                                    </option>
                                ))}
                            </select>

                            <input
                                type="text"
                                placeholder="חפש טקסט"
                                value={searchText}
                                onChange={(e) => setSearchText(e.target.value)}
                                className="search-input-text"
                            />
                        </div>
                    )}

                    {searchType === 'date' && (
                        <div className="date-search">
                            <select
                                value={selectedCourse}
                                onChange={handleCourseSelection}
                                className="search-input-course"
                                required
                            >
                                <option value="">בחר קורס</option>
                                {courses.map((course) => (
                                    <option key={course.course_id} value={course.course_id}>
                                        {course.name}
                                    </option>
                                ))}
                            </select>

                            <input
                                type="text"
                                placeholder="שנה"
                                value={examYear}
                                onChange={(e) => setExamYear(e.target.value)}
                                className="search-input-course"
                                disabled={selectedCourse === ''}
                            />

                            <select
                                value={examSemester}
                                onChange={(e) => setExamSemester(e.target.value)}
                                className="search-input-course"
                                disabled={examYear === ''}
                            >
                                <option value="">בחר סמסטר</option>
                                {semesters.map((semesterOption, index) => (
                                    <option key={index} value={semesterOption}>
                                        {semesterOption}
                                    </option>
                                ))}
                            </select>

                            <select
                                value={examDateSelection}
                                onChange={(e) => setExamDateSelection(e.target.value)}
                                className="search-input-course"
                                disabled={examSemester === ''}
                            >
                                <option value="">בחר מועד</option>
                                {examDates.map((dateOption, index) => (
                                    <option key={index} value={dateOption}>
                                        {dateOption}
                                    </option>
                                ))}
                            </select>

                            <input
                                type="number"
                                placeholder="מספר שאלה"
                                value={questionNum}
                                onChange={(e) => setQuestionNum(e.target.value)}
                                className="search-input-course"
                                disabled={examDateSelection === ''}
                            />
                        </div>
                    )}
                    <button className="search-button-home" onClick={handleSearch}>
                        חפש
                    </button>
                </div>
                <div className="search-results">
                    {searchResults.length > 0 ? (
                        <div>
                            <h3>התוצאות שהתקבלו</h3> {/* כותרת התוצאות */}
                            <ul className="results-list">
                                {searchResults.map((result) => (
                                    <li key={result.question_id} className="result-item">
                                        <a href={`/question/${result.course_id}/${result.year}/${result.semester}/${result.moed}/${result.question_number}`} className="result-link">
                                            <span>{courseIdToNameMap[result.course_id] || "לא ידוע"}_{result.year}_סמסטר-{result.semester}_מועד-{result.moed}_שאלה-{result.question_number}</span>
                                        </a>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ) : (
                        <div>
                            <h3>התוצאות שהתקבלו</h3>
                            <p>לא נמצאו תוצאות לחיפוש זה</p>
                        </div>
                    )}
                </div>

                <div className="action-buttons">
                    <button className="action-button">
                        <span>העלאת מבחן חדש</span>
                    </button>
                    <button className="action-button" onClick={openQuestionModal}>
                        <span>העלאת שאלה חדשה</span>
                    </button>
                    {isQuestionModalOpen && (
                        <div className="modal">
                        <div className="modal-content-question">
                            <p>
                                במידה והקורס לא נמצא ברשימת הקורסים, תוכל לפתוח אותו    
                                <a href="/opencourse"> כאן </a>.
                            </p>
                            <select
                                value={courseForQuestion}
                                onChange={handleCourseSelectionForQuestion}
                                className="search-input-course">
                                <option value="">בחר קורס</option>
                                {courses.map((course) => (
                                    <option key={course.course_id} value={course.course_id}>
                                        {course.name}
                                    </option>
                                ))}
                            </select>
                            <div className="modal-buttons">
                                <button class="confirm-button-question" onClick={navigateToUploadQuestion}>
                                    אישור
                                </button>
                                <button class="confirm-button-question" onClick={closeQuestionModal}>
                                    ביטול
                                </button>
                            </div>
                        </div>
                        </div>
                    )}
                </div>
                <div className="course-search-container">
                    <label className="search-label" htmlFor="courseId">חפש קורס:</label>
                    <input
                        type="text"
                        id="courseId"
                        placeholder="הכנס מזהה קורס (XXX.X.XXXX)"
                        value={courseId}
                        onChange={(e) => setCourseId(e.target.value)}
                        className="search-input-course"
                    />
                    <button className="search-button-home" onClick={() => handleCourseSearch(courseId)}>חפש קורס</button>
                </div>

                <div className="courses-section">
                    <h3>הקורסים שלי</h3>
                    <div className="course-cards-container">
                        {userCourses.map((course) => (
                            <div
                                key={course.id}
                                className="course-card"
                                onClick={() => handleCourseSearch(course.course_id)} // קריאה לפונקציה של החיפוש
                                >
                                <span>{course.name}</span>
                                <p style={{ fontSize: '12px', color: 'gray' }}>
                                    {course.id}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>

                {isCourseNotFoundModalOpen && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h2>הקורס לא נמצא</h2>
                        <p>האם תרצה לפתוח קורס חדש?</p>
                        <div className="modal-buttons">
                            <button onClick={navigateToAddNewCourse}>כן, פתח קורס חדש</button>
                            <button onClick={closeCourseNotFoundModal}>לא, ביטול</button>
                        </div>
                    </div>
                </div>
            )}


                <div className="add-course-button" onClick={navigateToAddNewCourse}>
                    <span className="plus-sign">+</span>
                    <span>פתיחת קורס חדש</span>
                </div>
            </main>
            <Footer />
        </div>
    );
}

export default Home;
