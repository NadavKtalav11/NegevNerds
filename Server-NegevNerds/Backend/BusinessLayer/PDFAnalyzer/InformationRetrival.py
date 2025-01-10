
from bidi.algorithm import get_display
import arabic_reshaper
import re
import pdfplumber
from collections import defaultdict
from Backend.DataLayer.WordsQuestions.WordsQuestionsRepository import WordsQuestionsRepository


class WordIndexController:
    def __init__(self, common_words_en, common_words_he):
        # self.english_dict = defaultdict(list)  # English word dictionary
        # self.hebrew_dict = defaultdict(list)   # Hebrew word dictionary
        self.common_words_en = set(common_words_en)  # Set of common English words
        self.common_words_he = set(common_words_he)  # Set of common Hebrew words
        self.words_repository = WordsQuestionsRepository()
        self.wordIndex1 = WordIndex1(common_words_en, common_words_he)
        self.wordIndex2 = WordIndex2(common_words_en, common_words_he)

    def process_pdf(self, pdf_file_path, question_id, course_id):
        # Process PDF using both WordIndex classes
        # english_words1, hebrew_words1 = self.wordIndex1.process_pdf(pdf_file_path, question_data)
        # english_words2, hebrew_words2 = self.wordIndex2.process_pdf(pdf_file_path, question_data)
        words1 = self.wordIndex1.process_pdf(pdf_file_path)
        words2 = self.wordIndex2.process_pdf(pdf_file_path)
        total_words = set(words1+words2)

        self.update_words(words=total_words, question_id=question_id, course_id=course_id)

    def process_photo(self, text, question_id , course_id):
        # Process PDF using both WordIndex classes
        # english_words1, hebrew_words1 = self.wordIndex1.process_pdf(pdf_file_path, question_data)
        # english_words2, hebrew_words2 = self.wordIndex2.process_pdf(pdf_file_path, question_data)

        english_words = re.findall(r'\b[a-zA-Z]+(?:-[a-zA-Z]+)?\b', text)

        # Regex for Hebrew words, including hyphenated ones
        hebrew_words = re.findall(r'\b[א-ת]+(?:-[א-ת]+)?\b', text)

        split_english = []
        for word in english_words:
            if '-' in word:
                split_english.extend(word.split('-'))
            else:
                split_english.append(word)

        # Process Hebrew words
        split_hebrew = []
        for word in hebrew_words:
            if '-' in word:
                split_hebrew.extend(word.split('-'))
            else:
                split_hebrew.append(word)

        words = split_english + split_hebrew
        words_set = set(words)

        self.update_words(words=words_set, question_id=question_id, course_id=course_id)



    def update_words(self, words, question_id, course_id):
        for word in words:
            word = word.lower()
            if len(word)>1:
                if word not in self.common_words_en and word not in self.common_words_he:
                    self.words_repository.add_word_to_question(word, question_id, course_id)



    def search_free_text(self, text: str) -> list:
        """
        Search for the 50 best matching question IDs based on the number of words in common with the text.

        :param text: The input free-text string.
        :return: A list of up to 50 question IDs with the most words in common with the text.
        """
        from collections import defaultdict

        # Step 1: Split the input text into words
        words = text.split()  # You may want to preprocess (e.g., lowercase, remove punctuation) as needed.

        # Step 2: Dictionary to count the number of matching words for each question ID
        dto_count = defaultdict(int)

        # Step 3: Iterate over words and fetch associated question IDs
        for word in words:
            search_dtos = self.words_repository.get_search_dto_by_word(word)
            for dto in search_dtos:
                dto_count[dto] += 1

            # Step 4: Sort SearchDTOs by frequency (descending), with a secondary sort by course ID and question ID
        sorted_dtos = sorted(
            dto_count.items(),
            key=lambda item: (-item[1], item[0].course_id, item[0].question_id)
            # Primary sort by count, then course/question IDs
        )

        # Step 5: Extract the top 50 SearchDTOs
        top_50_dtos = [dto for dto, _ in sorted_dtos[:50]]

        return top_50_dtos


    def search_free_text_with_course(self, text, course_id) -> list:
        """
        Search for the 50 best matching question IDs based on the number of words in common with the text.

        :param text: The input free-text string.
        :return: A list of up to 50 question IDs with the most words in common with the text.
        """
        from collections import defaultdict

        # Step 1: Split the input text into words
        words = text.split()  # You may want to preprocess (e.g., lowercase, remove punctuation) as needed.

        # Step 2: Dictionary to count the number of matching words for each question ID
        question_word_count = defaultdict(int)

        # Step 3: Iterate over words and fetch associated question IDs
        for word in words:
            question_ids = self.words_repository.get_questions_id_by_word_and_course(word, course_id)
            for question_id in question_ids:
                question_word_count[question_id] += 1

        # Step 4: Sort question IDs by the number of matching words (descending)
        # If counts are equal, secondary sorting by question ID (optional)
        sorted_questions = sorted(
            question_word_count.items(),
            key=lambda item: (-item[1], item[0])  # Sort by count descending, then by ID ascending
        )

        # Step 5: Extract the top 50 question IDs
        top_50_questions = [question_id for question_id, _ in sorted_questions[:50]]

        return top_50_questions



    


class WordIndex1:
    def __init__(self, common_words_en, common_words_he):
        self.hebrew_characters = re.compile(r'[\u0590-\u05FF]')
        self.hebrew_pattern = re.compile(r'[\u0590-\u05FF\uFB1D-\uFB4F]+')
        self.english_dict = defaultdict(list)
        self.hebrew_dict = defaultdict(list)
        self.common_words_en = set(common_words_en)
        self.common_words_he = set(common_words_he)

    def extract_words(self, text):
        if text is None:
            return [],[]

        # Regex for English words, including hyphenated ones
        english_words = re.findall(r'\b[a-zA-Z]+(?:-[a-zA-Z]+)?\b', text)

        # Regex for Hebrew words, including hyphenated ones
        hebrew_words = re.findall(r'\b[א-ת]+(?:-[א-ת]+)?\b', text)

        # Additionally, include components of hyphenated words
        split_english = []
        for word in english_words:
            if '-' in word:
                split_english.extend(word.split('-'))  # Add components of hyphenated words
            split_english.append(word)  # Keep the hyphenated word itself

        split_hebrew = []
        for word in hebrew_words:
            if '-' in word:
                split_hebrew.extend(word.split('-'))  # Add components of hyphenated words
            split_hebrew.append(word)  # Keep the hyphenated word itself

        return split_english , split_hebrew


    # def process_pdf(self, pdf_file_path):
    #     # Parse the PDF
    #     parsed = parser.from_file(pdf_file_path)
    #     text = parsed.get('content', '')
    #     normalized_text = self.normalize_text_direction(text)
    #     # Extract English and Hebrew words
    #     english_words, hebrew_words = self.extract_words(normalized_text)
    #     #print(hebrew_words)
    #     #reversed_hebrew_words = ["".join(reversed(word)) for word in hebrew_words]
    #     print ("rev" , hebrew_words)
    #     return english_words + hebrew_words

    def process_pdf(self, pdf_file_path):
        try:
            with pdfplumber.open(pdf_file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + " "

            normalized_text = self.normalize_mixed_text(text)
            english_words, hebrew_words = self.extract_words(normalized_text)
            print("proc" , hebrew_words)
            return english_words + hebrew_words

        except Exception as e:
            print(f"Error processing PDF: {e}")
            return []

    def normalize_mixed_text(self, text):
        # Split into lines to preserve structure
        lines = text.split('\n')
        normalized_lines = []

        for line in lines:
            # Process each line separately
            reshaped_text = arabic_reshaper.reshape(line)
            bidi_text = get_display(reshaped_text)
            normalized_lines.append(bidi_text)

        return '\n'.join(normalized_lines)

    # def extract_words(self, text):
    #     words = text.split()
    #     english_words = []
    #     hebrew_words = []
    #
    #     for word in words:
    #         if self.hebrew_pattern.search(word):
    #             hebrew_words.append(word)
    #         else:
    #             english_words.append(word)
    #
    #     return english_words, hebrew_words


    # def normalize_text_direction(self, text):
    #     """Normalize RTL directionality in mixed-language text."""
    #     lines = text.split("\n")
    #     normalized_lines = []
    #
    #     for line in lines:
    #         if self.contains_hebrew(line):
    #             # Reverse only Hebrew text for RTL consistency
    #             normalized_lines.append(self.reverse_hebrew_words(line))
    #         else:
    #             # Add LTR lines as-is
    #             normalized_lines.append(line)
    #
    #     return "\n".join(normalized_lines)
    #
    # def contains_hebrew(self, text):
    #     """Check if a string contains Hebrew characters."""
    #     return bool(self.hebrew_characters.search(text))
    #
    # def reverse_hebrew_words(self, line):
    #     """Reverse Hebrew words in the line while preserving order for non-Hebrew words."""
    #     words = line.split()
    #     reversed_words = []
    #     for word in words:
    #         if self.contains_hebrew(word):
    #             reversed_words.append(word[::-1])  # Reverse Hebrew word
    #         else:
    #             reversed_words.append(word)  # Keep non-Hebrew word as-is
    #     return " ".join(reversed_words)
        
    # def get_sorted_dictionaries(self):
    #     # Return sorted versions of both dictionaries
    #     sorted_english_dict = dict(sorted(self.english_dict.items()))
    #     sorted_hebrew_dict = dict(sorted(self.hebrew_dict.items()))
    #     return sorted_english_dict, sorted_hebrew_dict


    # def reverse_word_if_needed(self, word):
    #     # Reverse the word only if it is not in the correct direction (LTR -> RTL issue)
    #     if word != word[::-1]:  # This checks if the word is reversed (LTR).
    #         return word[::-1]
    #     return word


class WordIndex2:
    def __init__(self, common_words_en, common_words_he):
        self.hebrew_characters = re.compile(r'[\u0590-\u05FF]')
        self.english_dict = defaultdict(list)
        self.hebrew_dict = defaultdict(list)
        self.common_words_en = set(common_words_en)
        self.common_words_he = set(common_words_he)

  
    def extract_words(self, text):
        if text is None:
            return [], []

        # Regex for English words, including hyphenated ones
        english_words = re.findall(r'\b[a-zA-Z]+(?:-[a-zA-Z]+)?\b', text)

        # Regex for Hebrew words, including hyphenated ones
        hebrew_words = re.findall(r'\b[א-ת]+(?:-[א-ת]+)?\b', text)

        # Additionally, include components of hyphenated words
        split_english = []
        for word in english_words:
            if '-' in word:
                split_english.extend(word.split('-'))
            split_english.append(word)

        split_hebrew = []
        for word in hebrew_words:
            if '-' in word:
                split_hebrew.extend(word.split('-'))
            split_hebrew.append(word)

        return split_english, split_hebrew

    def process_pdf(self, pdf_file_path):
        try:
            with pdfplumber.open(pdf_file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + " "  # Combine text from all pages


            normalized_text = self.normalize_text_direction(text)

            # Extract English and Hebrew words
            english_words, hebrew_words = self.extract_words(normalized_text)
            # Extract English and Hebrew words
            # english_words, hebrew_words = self.extract_words(text)
            #
            # reversed_hebrew_words = [self.reverse_word_if_needed(word) for word in hebrew_words]

            #return english_words + reversed_hebrew_words
            print("nor" , hebrew_words)
            return english_words + hebrew_words

        except Exception as e:
            print(f"Error processing PDF: {e}")

    def normalize_text_direction(self, text):
        """Normalize RTL directionality in mixed-language text."""
        lines = text.split("\n")
        normalized_lines = []

        for line in lines:
            if self.contains_hebrew(line):
                # Reverse only Hebrew text for RTL consistency
                normalized_lines.append(self.reverse_hebrew_words(line))
            else:
                # Add LTR lines as-is
                normalized_lines.append(line)

        return "\n".join(normalized_lines)

    def contains_hebrew(self, text):
        """Check if a string contains Hebrew characters."""
        return bool(self.hebrew_characters.search(text))

    def reverse_hebrew_words(self, line):
        """Reverse Hebrew words in the line while preserving order for non-Hebrew words."""
        words = line.split()
        reversed_words = []
        for word in words:
            if self.contains_hebrew(word):
                reversed_words.append(word[::-1])  # Reverse Hebrew word
            else:
                reversed_words.append(word)  # Keep non-Hebrew word as-is
        return " ".join(reversed_words)

    # def process_text(self, text):
    #     # Tokenize the text
    #     heb_tokenizer = tokenizer()
    #     tokens = heb_tokenizer.tokenize(text)
    #     processed_words = []
    #
    #     for token in tokens:
    #         token_type, token_text = token
    #
    #         # Handle different token types
    #         if token_type in ['HEBREW', 'HEBREW_WITH_ENGLISH']:
    #             processed_words.append(token_text)
    #         elif token_type == 'ENGLISH':
    #             processed_words.append(token_text)
    #
    #     return processed_words

    # def is_hebrew(self, word):
    #     return all(0x590 <= ord(char) <= 0x5FF for char in word)
    #
    # def reverse_hebrew_word(self, word):
    #     # Reverse the Hebrew word if needed
    #     return "".join(reversed(word))
    #
    # def reverse_word_if_needed(self, word):
    #     # Reverse the word only if it is not in the correct direction (LTR -> RTL issue)
    #     if word != word[::-1]:  # This checks if the word is reversed (LTR).
    #         return word[::-1]
    #     return word