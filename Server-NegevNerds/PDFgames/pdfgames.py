from PyPDF2 import PdfReader, PdfWriter
import re
import os

def extract_text_from_pdf(pdf_path):
    """חילוץ טקסט מכל עמודי ה-PDF"""
    reader = PdfReader(pdf_path)
    text_pages = []
    for page in reader.pages:
        text_pages.append(page.extract_text())
    return text_pages

def extract_metadata(text):
    """חילוץ נתוני מטא מתוך הטקסט"""
    metadata = {
        "course_name": re.search(r"שם הקורס[:\s]*(.*)", text).group(1).strip() if re.search(r"שם הקורס[:\s]*(.*)", text) else "Not Found",
        "course_number": re.search(r"מספר הקורס[:\s]*(.*)", text).group(1).strip() if re.search(r"מספר הקורס[:\s]*(.*)", text) else "Not Found",
        "year": re.search(r"שנה[:\s]*(\d{4})", text).group(1).strip() if re.search(r"שנה[:\s]*(\d{4})", text) else "Not Found",
        "semester": re.search(r"סמסטר[:\s]*(.*)", text).group(1).strip() if re.search(r"סמסטר[:\s]*(.*)", text) else "Not Found",
        "moed": re.search(r"מועד[:\s]*(.*)", text).group(1).strip() if re.search(r"מועד[:\s]*(.*)", text) else "Not Found",
    }
    return metadata

def split_questions(pdf_path, output_folder):
    """פיצול ה-PDF לשאלות ושמירת כל שאלה כ-PDF נפרד"""
    os.makedirs(output_folder, exist_ok=True)

    reader = PdfReader(pdf_path)
    question_files = []

    writer = None
    current_question_start = None

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        print(f"Processing Page {page_num+1}:\n{text[:100]}")

        # בדיקה אם העמוד מכיל התחלה של שאלה חדשה
        if re.search(r"(?:\d+\.\s|שאלה\s*\d+|Question\s*\d+)", text):
            print(f"Found question start on page {page_num+1}")
            
            # סגור ושמור את השאלה הנוכחית אם יש
            if writer and current_question_start is not None:
                output_file = os.path.join(output_folder, f"question_{current_question_start + 1}.pdf")
                with open(output_file, "wb") as f:
                    writer.write(f)
                question_files.append(output_file)

            # התחל שאלה חדשה
            writer = PdfWriter()
            current_question_start = page_num

        # הוסף את העמוד הנוכחי לשאלה הנוכחית
        if writer:
            writer.add_page(page)

    # שמור את השאלה האחרונה
    if writer and current_question_start is not None:
        output_file = os.path.join(output_folder, f"question_{current_question_start + 1}.pdf")
        with open(output_file, "wb") as f:
            writer.write(f)
        question_files.append(output_file)

    return question_files

# הגדרת נתיב לקובץ ה-PDF ולתיקיית פלט
pdf_path = "C:/Users/noaab/limud/final_proj/NegevNerds/PDFgames/modelim2018.pdf"
output_folder = "C:/Users/noaab/limud/final_proj/NegevNerds/PDFgames/output_questions"

# חילוץ טקסט מעמודי ה-PDF
text_pages = extract_text_from_pdf(pdf_path)

# חילוץ נתוני מטא מהעמוד הראשון
metadata = extract_metadata(text_pages[0])

# פיצול ה-PDF לשאלות
question_files = split_questions(pdf_path, output_folder)

# תוצאות
print("Metadata Extracted:")
print(metadata)
print("Questions Saved as PDFs:")
for file in question_files:
    print(file)
