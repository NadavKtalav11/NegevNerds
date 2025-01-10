from PyPDF2 import PdfReader, PdfWriter
import re
import os
import pdfplumber
from tabula import read_pdf
import pandas as pd

class Course_syllabus:
    def __init__(self):
        pass

    def extract_syllabus_topic_total(self, pdf_path):
        topic_patterns = [
        r'סילבוס[:\n](.*?)\n',  # Hebrew pattern for "Syllabus"
        r'סילבוס באנגלית[:\n](.*?)\n',
        r'סילבוס בעברית[:\n](.*?)\n',
    ]
        topic_patterns1 = [
        r'נושאים[:\n](.*?)\n',  # Hebrew pattern for "Topics"
        r'Course Topics[:\n](.*?)\n',
        r'Outline[:\n](.*?)\n',
    ]
        
        topics_table = ["נושאי השיעור", "נושא השיעור","Topics", "Outline","Lecture", "Practical Session"]  # List of column headers to search for

        topics = set()
        cropped_pdf_path = self.crop_pdf_top_margin(pdf_path)
        has_table = self.has_valid_table_with_pdfplumber(cropped_pdf_path)
        if not has_table:
            topics = self.extract_syllabus_topics_with_pdfplumber(cropped_pdf_path,topic_patterns)
            if len(topics)==0:
                topics = self.extract_syllabus_topics_with_pdfplumber(cropped_pdf_path,topic_patterns1)
        else:
            topics = self.extract_table_with_topics_final(cropped_pdf_path,topics_table )
        cleaned_topics = set()
        for topic in topics:
            # Remove leading numbers (e.g., "1.", "2. ", etc.)
            topic = re.sub(r"^\d+\.\s*", "", topic)
            # Remove leading special characters like "•", "*", etc.
            topic = topic.lstrip("•* ").strip()
            if topic:  # Only keep non-empty topics
                cleaned_topics.add(topic)
        cleaned_topics = {topic for topic in cleaned_topics if re.search(r"[a-zA-Zא-ת]", topic)}

        # Delete the cropped PDF file
        if os.path.exists(cropped_pdf_path):
            os.remove(cropped_pdf_path)
        

        return cleaned_topics


    
    def has_valid_table_with_pdfplumber(self, pdf_path, min_rows=2, min_columns=2):
        """
        Checks if a PDF contains at least one valid table using pdfplumber.

        :param pdf_path: Path to the PDF file
        :param min_rows: Minimum number of rows to validate a table
        :param min_columns: Minimum number of columns to validate a table
        :return: True if at least one valid table is found, False otherwise
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    tables = page.extract_tables()  # Extract tables from the page
                    if tables:
                        for table in tables:
                            # Validate table structure
                            if len(table) >= min_rows and len(table[0]) >= min_columns:
                                return True
            return False
        except Exception as e:

            return False


  

    def extract_syllabus_topics_with_pdfplumber(self, file_path, topic_patterns):
        """
        Extracts syllabus topics from a course PDF file using pdfplumber and returns them as a set.
        Handles diverse formats such as tables, bullet points, numbered sections, and headers.

        :param file_path: Path to the PDF file
        :param topic_patterns: List of regex patterns to identify syllabus-related sections
        :return: A set of topics from the syllabus
        """
        syllabus_topics = set()
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        # Match topics using provided patterns
                        for pattern in topic_patterns:
                            matches = re.findall(pattern, text, re.DOTALL)
                            for match in matches:
                                # Split potential topics by common delimiters and clean up
                                topics = re.split(r',|;|\n|\•|\.', match)
                                syllabus_topics.update([topic.strip() for topic in topics if topic.strip()])

                        # Handle bullet points
                        lines = text.split("\n")
                        for line in lines:
                            if re.match(r'^\•', line):  # Matches lines starting with "•"
                                syllabus_topics.add(line.lstrip("• ").strip())

                        # Handle numbered sections (e.g., "1. Topic", "2. Topic")
                        for line in lines:
                            if re.match(r'^\d+\.\s', line):  # Matches lines starting with "1. ", "2. ", etc.
                                syllabus_topics.add(line.strip())

                        # Handle keywords directly in the text
                        if any(keyword in text for keyword in ["סילבוס", "Topics", "Outline"]):
                            for line in lines:
                                # Add lines containing relevant keywords as potential topics
                                if any(keyword in line for keyword in ["סילבוס", "Topics", "Outline"]):
                                    syllabus_topics.add(line.strip())
        except Exception as e:
            print(f"Error processing PDF with pdfplumber: {e}")

        return syllabus_topics


    
    
    def extract_table_with_topics_final(self,pdf_path, topics, pages="all"):
        """
        Extracts tables from a PDF, matches column titles to a list of topics,
        and returns data under matching columns.

        :param pdf_path: Path to the PDF file
        :param topics: List of column titles to match
        :param pages: Pages to extract tables from (default: "all")
        :return: Set of data under matching columns
        """
        matching_data = set()

        try:
            # Extract tables using Tabula
            # tables = read_pdf(pdf_path, pages=pages, multiple_tables=True, pandas_options={"header": None}, encoding="ISO-8859-8")
            tables = read_pdf(pdf_path, pages=pages, multiple_tables=True, pandas_options={"header": None})

            if not tables:
                return matching_data

            for i, table in enumerate(tables):

                # Assume the first row is the header
                df = pd.DataFrame(table)
                headers = df.iloc[0]
                df.columns = headers
                df = df[1:]  # Remove the header row

                # Clean up headers for matching
                df.columns = df.columns.str.strip()


                # Check for matching columns
                for column in df.columns:
                    if any(topic in column for topic in topics):
                        matching_data.update(df[column].dropna().tolist())

        except Exception as e:
            print(f"Error during table extraction: {e}")

        return matching_data
    


    def crop_pdf_top_margin(self, pdf_path, margin_cm=4.0):
        """
        Crops a specified top margin (in centimeters) from all pages of a PDF,
        saves the result in the same directory with '_cropped' appended to the file name,
        and returns the path to the new PDF.
        
        :param pdf_path: Path to the original PDF file.
        :param margin_cm: Top margin to crop, specified in centimeters.
        :return: Path to the cropped PDF.
        """
        # Convert centimeters to points (1 cm = 28.35 points)
        cm_to_points = margin_cm * 28.35

        # Prepare output file path (same directory, _cropped appended)
        dir_name = os.path.dirname(pdf_path)
        base_name = os.path.basename(pdf_path).replace('.pdf', '_cropped.pdf')
        output_path = os.path.join(dir_name, base_name)

        # Initialize PDF writer
        pdf_writer = PdfWriter()

        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                width, height = page.width, page.height
                # Crop the top margin
                cropped_page_bbox = (0, cm_to_points, width, height)

                # Use PyPDF2 to adjust page size
                reader = PdfReader(pdf_path)
                page_to_write = reader.pages[i]
                page_to_write.mediabox.upper_left = (0, height - cm_to_points)

                # Add the adjusted page to the writer
                pdf_writer.add_page(page_to_write)

        # Save the cropped PDF to the same directory
        with open(output_path, "wb") as out_file:
            pdf_writer.write(out_file)

        print(f"Cropped PDF saved to: {output_path}")
        return output_path
