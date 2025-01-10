from tika import parser
from collections import defaultdict
import re

class WordTracker:
    def __init__(self):
        self.words = defaultdict(set)  # Dictionary to hold word and its PDF IDs

    def insert(self, word, pdf_id):
        self.words[word].add(pdf_id)  # Use a set to avoid duplicate PDF IDs

    def display(self):
        for word in sorted(self.words.keys()):  # Sort words alphabetically
            print(f"{word} (PDF IDs: {sorted(self.words[word])})")

    def search(self, query_words):
        results = {}
        for word in query_words:
            if word in self.words:
                results[word] = sorted(self.words[word])
        return results

# Global dictionary to hold PDF data with unique IDs
pdf_data = {}
pdf_counter = 0
word_tracker = WordTracker()

def extract_pdf_info(pdf_file_path):
    parsed = parser.from_file(pdf_file_path)
    metadata = parsed.get('metadata', {})
    text = parsed.get('content', '')
    return metadata, text

def extract_exam_details(text):
    if text is None:
        return None  # Return None if text is not valid
    course_match = re.search(r'שם הקורס:\s*(.+)', text)
    year_match = re.search(r'שנה:\s*(\d{4})', text)
    semester_match = re.search(r'סמסטר:\s*([AB])', text)
    moed_match = re.search(r'מועד:\s*([abc])', text)

    course = course_match.group(1).strip() if course_match else None
    year = year_match.group(1).strip() if year_match else None
    semester = semester_match.group(1).strip() if semester_match else None
    moed = moed_match.group(1).strip() if moed_match else None

    return (course, year, semester, moed)

def save_pdf_data(pdf_file_path):
    global pdf_counter
    pdf_counter += 1
    metadata, text = extract_pdf_info(pdf_file_path)

    pdf_data[pdf_counter] = {
        'metadata': metadata,
        'text': text,
        'exam_details': extract_exam_details(text)
    }

    # Check if text is valid before processing
    if text:
        words = re.findall(r'\b\w+\b', text.lower())
        for word in set(words):  # Use set to avoid duplicate words
            word_tracker.insert(word, pdf_counter)
    else:
        print(f"No content found in PDF ID: {pdf_counter}")

    print(f"Saved PDF ID: {pdf_counter}")

def main():
    pdf_file_paths = [
        "/Users/davidvolodarsky/Desktop/NegevNerds/os_2022_B_moedA.pdf",  # Add more PDF paths as needed
        "/Users/davidvolodarsky/Desktop/NegevNerds/ppl_2023_B.pdf"
    ]
    
    for pdf_file_path in pdf_file_paths:
        save_pdf_data(pdf_file_path)

    # Display the sorted words and their PDF IDs
    print("\nSorted List of Words:")
    # word_tracker.display()

    # Example search
    search_terms = ['never']  # Replace with your search terms
    search_results = word_tracker.search(search_terms)
    
    print("\nSearch Results:")
    for word, pdf_ids in search_results.items():
        print(f"{word}: {pdf_ids}")

if __name__ == "__main__":
    main()
