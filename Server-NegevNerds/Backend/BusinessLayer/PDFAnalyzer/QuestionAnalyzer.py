import fitz  # PyMuPDF
from PIL import Image
import pytesseract


class QuestionAnalyzer:

    def extract_text_from_pdf_file(self,file_obj):
        try:
            # Open the PDF from the file-like object
            document = fitz.open(stream=file_obj.read(), filetype="pdf")
            text = ""
            for page in document:
                text += page.get_text()
            document.close()
            return text
        except Exception as e:
            return f"An error occurred: {e}"

    def extract_text_from_image(self,  image_file):
        """
        Extracts text from an image using Tesseract OCR for Hebrew and English.

        :param image_path: Path to the image file
        :return: Extracted text as a string
        """
        try:
            # Open the image
            image = Image.open(image_file)

            # Perform OCR using Tesseract with Hebrew and English
            text = pytesseract.image_to_string(image, lang="heb+eng")
            # print(text)
            return text

        except Exception as e:
            print(f"Error occurred: {e}")
            return None





# if __name__ == "__main__":
#     image_path = "../../../photo2.jpg"  # Replace with your image path
#     extracted_text = extract_text_from_image(image_path)
#     print("Extracted Text:\n" , extracted_text)