// Footer.js
import React, { useState } from 'react';
import './Footer.css';

function Footer() {
    const [showModal, setShowModal] = useState(false); // ניהול מצב המודל
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

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

    // הצגת המודל
    const handleTermsOfUseClick = () => {
        setShowModal(true);
    };

    // סגירת המודל
    const handleCloseModal = () => {
        setShowModal(false);
    };

    return (
        <footer className="footer-container">
            <div className="footer-content">
                <div className="footer-section">
                    <h2><strong>NegevNerds</strong></h2>
                    <p>פלטפורמה ללמידה למבחנים עבור סטודנטים באוניברסיטת בן גוריון.</p>
                    <p>המערכת מציגה את המידע בצורה מאורגנת, כך שלא תבזבז יותר זמן בחיפוש אחרי שאלות ותשובות.</p>
                    <p><strong>רוצה להיות חנון אמיתי? הצטרף ל-NegevNerds ותראה איך להיות חנון עושה לך טוב!  
                    המערכת שלנו תשדרג את הלמידה ותשאיר אותך צעד לפני כולם, עם פלטפורמה נוחה, מאורגנת ונגישה –  
                    כי להיות חנון זה לא רק לדעת את החומר, אלא לדעת איך לנצל את הזמן שלך בצורה הכי חכמה.</strong></p>
                </div>

                <div className="footer-section">
                    <h3><strong>צור קשר</strong></h3>
                    <p><strong>שלח פידבק על המערכת:</strong></p>
                    <a href={`mailto:negevnerds@gmail.com`}><strong>negevnerds@gmail.com</strong></a>
                    <p><strong>או בטלפון (רק לבנות) 0545433476</strong></p>
                    <p><strong>שיהיו חזקים השאר</strong></p>
                </div>

                <div className="footer-section">
                    <h3><strong>קישורים חשובים</strong></h3>
                    {/* טקסט לחיץ */}
                    <p className="terms-link" onClick={handleTermsOfUseClick}>
                        <strong>תנאי שימוש</strong>
                    </p>
                    <p><strong>{`© 2024-2025 NegevNerds. כל הזכויות שמורות.`}</strong></p>
                </div>
            </div>

            {/* Modal תנאי שימוש */}
            {showModal && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h2>תנאי שימוש</h2>
                        <p>{termsOfUseContent}</p>
                        <button onClick={handleCloseModal}>סגור</button>
                    </div>
                </div>
            )}
        </footer>
    );
}

export default Footer;
