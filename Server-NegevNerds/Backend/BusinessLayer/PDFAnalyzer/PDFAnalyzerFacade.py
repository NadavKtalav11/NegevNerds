from Backend.BusinessLayer.PDFAnalyzer.Course_syllabus import Course_syllabus 
from Backend.BusinessLayer.PDFAnalyzer.InformationRetrival import * 




class PDFAnalyzerFacade:
    _instance = None  # Class-level attribute to hold the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Only initialize attributes if they don't already exist
        if not hasattr(self, 'course_syllabus'):
            self.course_syllabus = Course_syllabus()
        common_words_en = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours',
            'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',
            'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself',
            'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
             'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
             'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
             'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
            'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
            'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
            'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
            'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
            's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
             'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't",
            'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
             "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
            'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"}
        common_words_he = {'אני','את','אתה','אנחנו','אתן','אתם','הם','הן','היא','הוא','שלי','שלו',
            'שלך','שלה','שלנו','שלכם','שלכן','שלהם','שלהן','לי','לו','לה','לנו',
            'לכם','לכן','להם','להן','אותה','אותו','זה','זאת','אלה','אלו','תחת',
            'מתחת','מעל','בין','עם','עד','נגר','על','אל','מול','של','אצל','כמו','אחר',
            'אותו','בלי','לפני','אחרי','מאחורי','עלי','עליו','עליה','עליך','עלינו','עליכם',
            'לעיכן','עליהם','עליהן','כל','כולם','כולן','כך','ככה','כזה','זה','זות','אותי',
            'אותה','אותם','אותך','אותו','אותן','אותנו','ואת','את','אתכם','אתכן','איתי','איתו','איתך',
            'איתה','איתם','איתן','איתנו','איתכם','איתכן','יהיה','תהיה','היתי','היתה','היה','להיות','עצמי',
            'עצמו','עצמה','עצמם','עצמן','זו','עצמנו','עצמהם','עצמהן','מי','מה','איפה','היכן','במקום שבו','אם',
            'לאן','למקום שבו','מקום בו','איזה','מהיכן','איך','כיצד','באיזו מידה','מתי','בשעה ש','כאשר','כש',
            'למרות','לפני','אחרי','מאיזו סיבה','הסיבה שבגללה','למה','מדוע','לאיזו תכלית','כי','יש','אין','אך',
            'מנין','מאין','מאיפה','יכל','יכלה','יכלו','יכול','יכולה','יכולים','יכולות','יוכלו','יוכל','מסוגל',
            'לא','רק','אולי','אין','לאו','אי','כלל','נגד','אם','עם','אל','אלה','אלו','אף','על','מעל','מתחת','מצד','בשביל',
            'לבין','באמצע','בתוך','דרך','מבעד','באמצעות','למעלה','למטה','מחוץ','מן','לעבר','מכאן',
            'כאן','הנה','הרי','פה','שם','אך','ברם','שוב','אבל','מבלי','בלי','מלבד','רק','בגלל','מכיוון','עד','אשר',
            'ואילו','למרות','אס','כמו','כפי','אז','אחרי','כן','לכן','לפיכך','מאד','עז','מעט','מעטים','במידה','שוב',
            'יותר','מדי','גם','כן','נו','להלן','לפי','אחר','אחרת','אחרים','אחרות','אשר','או'}

        self.inforamtion_retrival =  WordIndexController(common_words_en,common_words_he)


    def extract_syllabus_topic_total(self, pdf_path):
        syllabus = self.course_syllabus.extract_syllabus_topic_total(pdf_path)
        return syllabus
    
    def perform_information_retrival_question_pdf(self, pdf_question_path, question_id, course_id):
        self.inforamtion_retrival.process_pdf(pdf_file_path=pdf_question_path , question_id=question_id, course_id=course_id)

    def perform_information_retrival_question_photo(self, text, question_id , course_id):

        self.inforamtion_retrival.process_photo(text=text, question_id=question_id, course_id=course_id)

    def search_free_text(self , text):
        return self.inforamtion_retrival.search_free_text(text=text)

    def search_free_text_from_course(self , text, course_id):
        return self.inforamtion_retrival.search_free_text_with_course(text=text, course_id = course_id)


       