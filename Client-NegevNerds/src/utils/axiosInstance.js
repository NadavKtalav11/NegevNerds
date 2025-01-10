import axios from 'axios';

// יצירת axios instance
const axiosInstance = axios.create({
    baseURL: 'http://localhost:5001/api/',  // כתובת ה-API של השרת
    headers: {
        'Content-Type': 'application/json',
    }
});

// Interceptor למקרה של טוקן פג תוקף
axiosInstance.interceptors.response.use(
    response => response,  // החזרת תוצאות מוצלחות
    async (error) => {
        if (error.response && (error.response.status === 422 || error.response.status === 401)) {
            // טוקן פג תוקף או לא תקין
            console.log("Token expired or invalid. Redirecting to login page.");
            alert("Your session has expired or your token is invalid. Please log in again.");
            // מחיקת הטוקן והפנייה לדף התחברות
            localStorage.clear();  // ניקוי כל ה-localStorage
            window.location.href = '/login';  // הפנייה לדף התחברות
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;
