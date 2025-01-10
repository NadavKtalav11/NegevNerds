import React, { useState } from 'react';
import './OpenCourse.css'; // יש לוודא שהקובץ הזה קיים
import Header from '../Header/Header'; // נניח שאתה משתמש בהדר ב-header עצמאי
import Footer from '../Footer/Footer';  // ייבוא הפוטר
import axios from 'axios'; // Ensure Axios is imported
import axiosInstance from '../../utils/axiosInstance';



function OpenCourse() {
  const [newCourseNumber, setNewCourseNumber] = useState('');
  const [newCourseName, setNewCourseName] = useState('');
  const [syllabusFile, setSyllabusFile] = useState(null);
  const [showCourseNumberTooltip, setShowCourseNumberTooltip] = useState(false); // Tooltip state
  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

  const handleNewCourseSubmit = async () => {
    if (!newCourseNumber || !newCourseName || !syllabusFile) {
      alert('כל השדות חובה'); // Validate all fields
      return;
    }
  
    // Retrieve user_id dynamically
    // const userId = localStorage.getItem('user_id');
    // if (!userId) {
    //   alert('User ID is missing. Please log in again.');
    //   return;
    // }
  
    try {
      // Create a FormData instance
      const formData = new FormData();
      formData.append('course_id', newCourseNumber); // Course ID
      // formData.append('user_id', userId);            // User ID
      formData.append('name', newCourseName);        // Course Name
      formData.append('syllabus_content_pdf', syllabusFile); // Syllabus PDF file
  
      // Send FormData to backend
      const response = await axiosInstance.post(
        `${API_BASE_URL}/api/course/open_course`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,  // Send token in header
          },
        }
      );
  
      // Handle success
      if (response.data.success) {
        alert('הקורס נוסף בהצלחה!'); // Success message
        console.log('Response:', response.data); // Log response for debugging
      } else {
        alert(`שגיאה: ${response.data.message}`); // Backend error message
      }
    } catch (error) {
      console.error('Error adding course:', error); // Log error
      alert('שגיאה בהוספת הקורס. אנא נסה שוב מאוחר יותר.'); // General error alert
    }
  };
  

  return (
    <div className="open-course-page">
      <Header />
      <main className="content">
        <div className="form-content">
          <h2>הוספת קורס חדש</h2>
          <div className="input-container">
            <input
              type="text"
              placeholder="מספר קורס"
              value={newCourseNumber}
              onChange={(e) => setNewCourseNumber(e.target.value)}
              onMouseEnter={() => setShowCourseNumberTooltip(true)}
              onMouseLeave={() => setShowCourseNumberTooltip(false)}
              className="search-input-open"
              required
            />
            {showCourseNumberTooltip && (
              <div className="tooltip">חובה מהצורה xxx.x.xxxx</div>
            )}
          </div>
          <input
            type="text"
            placeholder="שם קורס"
            value={newCourseName}
            onChange={(e) => setNewCourseName(e.target.value)}
            className="search-input-open"
            required
          />
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setSyllabusFile(e.target.files[0])}
            className="search-input-open"
            required
          />
          <button className="search-button" onClick={handleNewCourseSubmit}>
            הוסף קורס
          </button>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default OpenCourse;
