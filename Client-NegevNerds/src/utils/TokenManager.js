import { jwtDecode } from 'jwt-decode';

class TokenManager {
    static getToken() {
      return localStorage.getItem('access_token');
    }
  
    static setToken(token) {
      localStorage.setItem('access_token', token);
    }

    static getUserIdFromToken() {
        const token = TokenManager.getToken();
        if (token) {
          try {
            const decoded = jwtDecode(token);  // פענוח הטוקן
            return decoded.sub;  // מניח ש־sub הוא ה־user_id, ב־JWT בדרך כלל יש את ה־user_id במפתח זה
          } catch (error) {
            console.error("Invalid token:", error);
            return null;
          }
        }
        return null;
      }
  }
  
  export default TokenManager;
  