from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from Backend.DataLayer.Base import Base
from Backend.DataLayer.DTOs.SearchDTO import SearchDTO


#
# Base = declarative_base()


# Dynamically create table classes for each letter
def create_letter_model(letter, is_hebrew=False):
    table_name = f"{'hebrew' if is_hebrew else 'english'}letter{letter}"
    return type(f"Letter{letter}Model", (Base,), {
        '__tablename__': table_name,
        'word': Column(String,primary_key=True, nullable=False),
        'question_id': Column(String, primary_key=True),
        'course_id': Column(String)
    })


# Create model classes for all letters
MODELS = {}

# English letters
for letter in 'abcdefghijklmnopqrstuvwxyz':
    MODELS[letter] = create_letter_model(letter)

# Hebrew letters
for letter in 'פםןוטארקשדגכעיחלךףץתצמנהבסז':
    MODELS[letter] = create_letter_model(letter, is_hebrew=True)


class WordsQuestionsRepository:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), '../../..', 'NegevNerds.db')

        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_word_to_question(self, word, question_id, course_id):
        session = self.Session()
        first_letter= word[0]
        model = MODELS[first_letter]
        entry = model(word=word,question_id=question_id, course_id=course_id)
        try:
            session.add(entry)
            session.commit()
        except IntegrityError:
            session.rollback()  # Rollback the transaction if there's an error (duplicate entry)
            print(f"Word '{word}' with question_id '{question_id}' already exists. Skipping.")
        finally:
            session.close()

    def get_search_dto_by_word(self, word):
        session = self.Session()
        try:
            dtos = []
            first_letter = word[0]
            models = session.query(MODELS[first_letter]).filter_by(word=word).all()
            session.close()
            for model in models:
                dtos.append(SearchDTO(question_id=model.question_id, course_id=model.course_id))
            return dtos
        finally:
            session.close()


    def get_questions_id_by_word_and_course(self, word, course_id):
        session = self.Session()
        try:
            ids = []
            first_letter = word[0]
            models = session.query(MODELS[first_letter]).filter_by(word=word, course_id=course_id).all()
            session.close()
            for model in models:
                ids.append(model.question_id)
            return ids
        finally:
            session.close()

   

    def delete_question_words_from_all_tables(self, question_details):
        """
        Deletes all rows across all words tables defined in MODELS where question_id matches.

        Args:
            question_id (str): The ID of the question whose topics should be deleted.
        """
        session = self.Session()
        try:
            for letter, model_class in MODELS.items():
                try:
                    # Query the table associated with the model
                    rows_to_delete = session.query(model_class).filter_by(question_id=question_details).all()
                    
                    # Delete each row
                    for row in rows_to_delete:
                        session.delete(row)

                except Exception as e:
                    # Handle errors specific to the table, log and continue
                    print(f"Error deleting topics for table '{letter}': {str(e)}")

            # Commit all deletions
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(f"Error deleting topics across all tables: {str(e)}")
        finally:
            session.close()

