import smtplib
import random
import datetime
import os
import re
import threading
import uuid
from email.mime.text import MIMEText
import bcrypt
import logging
from Backend.BusinessLayer.User.User import User  # Adjusted import
from Backend.BusinessLayer.Util.Exceptions import *
from Backend.DataLayer.User.UserRepository import UserRepository  # Import the SQLAlchemy repository


class UserFacade:
    _instance = None  # Singleton pattern

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'users_byEmail'):  # Initialize only once
            self.users_byEmail = {}
            self.users_byId = {}
            self.pending_auth_codes = {}  # Stores pending auth codes and their expiry times
            self.auth_lock = threading.Lock()  # Lock for thread-safe access

            self.email_lock = threading.Lock()
            self.id_lock = threading.Lock()

    def generateUserId(self):
        return "user" + str(uuid.uuid4())

    def hash_password(self,password):
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def verify_password(self, provided_password, stored_hashed_password):
        """Verify a password against a stored hashed password."""
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hashed_password.encode('utf-8'))

    def is_valid_email(self,email):
        """Validate email domain."""
        return bool(re.match(r".+@(post\.bgu\.ac\.il|bgu\.ac\.il)$", email))

    def is_valid_name(self, name):
        """
        Validates a name to ensure it contains only Hebrew characters, spaces, tabs, and hyphens.

        Args:
        name (str): The name to validate.

        Returns:
        bool: True if the name is valid, False otherwise.
        """
        # Regular expression to allow only Hebrew characters, spaces, tabs, and hyphens
        hebrew_name_regex = r'^[\u0590-\u05FF]+([\s\t-][\u0590-\u05FF]+)*$'

        # Validate the name using regex
        return bool(re.match(hebrew_name_regex, name))

    def is_valid_password(self,password):
        """
        Validate the password.
        Password must:
        - Be at least 8 characters long
        - Be at most 20 characters long
        - Contain only English letters (a-z, A-Z), numbers, and allowed special characters
        - Contain at least one uppercase letter
        - Contain at least one lowercase letter
        - Contain at least one number
        - Contain at least one special character: {, }, [, ], !, @, $, %, ^, &, *, (, ), +
        """

        # Check for minimum and maximum length
        if len(password) < 8 or len(password) > 20:
            return False

        # Ensure password contains only allowed characters
        if not re.match(r"^[A-Za-z0-9{}\[\]!@\$%\^&\*\(\)\+]+$", password):
            return False

        # Regular expressions for each condition
        has_uppercase = re.search(r"[A-Z]", password)
        has_lowercase = re.search(r"[a-z]", password)
        has_number = re.search(r"[0-9]", password)
        has_special = re.search(r"[{}\[\]!@\$%\^&\*\(\)\+]", password)

        # Return True only if all conditions are met
        return bool(has_uppercase and has_lowercase and has_number and has_special)

    def register(self, email, password,password_confirm, first_name, last_name):
        """
        Unified register function.
        - Sends an authentication code.
        - Verifies the code interactively.
        - Completes the registration.
        """
        try:
            if self.getUser_by_email(email) is not None:
                raise Exception("המשתמש כבר קיים במערכת.")

            if not self.is_valid_name(first_name):
                raise Exception("השם הפרטי אינו תקין.")

            if not self.is_valid_name(last_name):
                raise Exception("שם המשפחה אינו תקין.")

            if not self.is_valid_email(email):
                raise Exception("האימייל אינו תקין.")

            if not self.is_valid_password(password):
                raise Exception("הסיסמה אינה תקינה.")

            if password != password_confirm:
                raise Exception("הסיסמה אינה תואמת לאימות סיסמה.")

            # Send authentication code
            self.send_auth_code(email, first_name)
            encrypt_password = self.hash_password(password)

            return encrypt_password, {"message": f"קוד אימות נשלח למייל {email}"}
        except Exception as e:
                raise Exception(str(e))

    def register_authentication_part(self, email, auth_code: str):
        # Interactively verify the code # Allow up to 3 attempts
        try:
            stored_code, expiry_time = self.pending_auth_codes[email]
            if auth_code == stored_code:
                if datetime.datetime.now() <= expiry_time:
                    return {"message": "עוברים למעבר על תנאי השימוש"}
                else:
                    logging.error("Authentication failed. The code has expired.")
                    raise Exception("אימות נכשל. הקוד פג תוקף.")
            else:
                logging.error("Incorrect authentication code.")
                raise Exception("קוד אימות שגוי.")
        except Exception as e:
            logging.error(f"Attempt  failed: {e}")
            raise Exception("האימות נכשל. הרשמה בוטלה.")

    def register_termOfUse_part(self, email, password, first_name, last_name):
        # Interactively verify the code
        with self.email_lock:
            with self.id_lock:
                try:
                        id = self.generateUserId()
                        user = User.create(id, email, password, first_name, last_name)
                        user.login()
                        self.users_byEmail[email] = user
                        self.users_byId[id] = user
                        logging.info(f"User {first_name} {last_name} registered successfully.")
                        return id, {"message": f"User {first_name} {last_name} registered successfully."}
                except Exception as e:
                        raise Exception("האישור נכשל. הרשמה בוטלה.")


    def get_user_name(self, user_id):
        curr_user = self.getUser_by_id(user_id=user_id)
        if curr_user is None:
            return []
        return curr_user.first_name + " " + curr_user.last_name

    def is_valid_email(self,email):
        """Validate email domain."""
        return bool(re.match(r".+@(post\.bgu\.ac\.il|bgu\.ac\.il)$", email))
    
    
    def is_valid_name(self, name):
        """
        Validates a name to ensure it contains only Hebrew characters, spaces, tabs, and hyphens.

        Args:
        name (str): The name to validate.

        Returns:
        bool: True if the name is valid, False otherwise.
        """
        # Regular expression to allow only Hebrew characters, spaces, tabs, and hyphens
        hebrew_name_regex = r'^[\u0590-\u05FF]+([\s\t-][\u0590-\u05FF]+)*$'
        
        # Validate the name using regex
        return bool(re.match(hebrew_name_regex, name))

    
    def is_valid_password(self,password):
        """
        Validate the password.
        Password must:
        - Be at least 8 characters long
        - Be at most 20 characters long
        - Contain only English letters (a-z, A-Z), numbers, and allowed special characters
        - Contain at least one uppercase letter
        - Contain at least one lowercase letter
        - Contain at least one number
        - Contain at least one special character: {, }, [, ], !, @, $, %, ^, &, *, (, ), +
        """

        # Check for minimum and maximum length
        if len(password) < 8 or len(password) > 20:
            return False

        # Ensure password contains only allowed characters
        if not re.match(r"^[A-Za-z0-9{}\[\]!@\$%\^&\*\(\)\+]+$", password):
            return False

        # Regular expressions for each condition
        has_uppercase = re.search(r"[A-Z]", password)
        has_lowercase = re.search(r"[a-z]", password)
        has_number = re.search(r"[0-9]", password)
        has_special = re.search(r"[{}\[\]!@\$%\^&\*\(\)\+]", password)

        # Return True only if all conditions are met
        return bool(has_uppercase and has_lowercase and has_number and has_special)
    
    def send_auth_code(self,email, first_name):
        """Generate and send an authentication code via email."""
        auth_code = random.randint(100000, 999999)
        auth_code = str(auth_code)
        auth_code_expiry = datetime.datetime.now() + datetime.timedelta(minutes=3)
        self.pending_auth_codes[email] =(auth_code, auth_code_expiry)

        sender_email = os.getenv("EMAIL_ADDRESS")
        sender_password = os.getenv("EMAIL_PASSWORD")
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        subject = "קוד האימות שלך"
        message = (f"שלום {first_name},\n\n"
                   f"קוד האימות שלך עבור NegevNerds הוא: {auth_code}\n"
                   f"הקוד תקף למשך 3 דקות.\n\n"
                   f"תודה רבה!")
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = email

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            logging.info(f"Authentication code sent to {email}")
        except Exception as e:
            logging.error(f"Failed to send authentication code: {e}")
            raise Exception("Failed to send authentication code.")

    # def login(self, email, password):
    #     """Authenticate the user by checking the email and password."""

    #     # Check if the email exists in the system
    #     user = self.users_byEmail.get(email)  # Use .get() to avoid KeyError
    #     if user is None:
    #         raise UserOrPasswordIncorrectError()

    #     # Check if the password matches
    #     if user.password != password:
    #         raise UserOrPasswordIncorrectError()

    #     user_id = user.id
    #     user_firstName = user.first_name
    #     user_lastName = user.last_name
    #     user.login()
    #     logging.info(f"Login successful for user: {email}")
    #     # message = "התחברות בוצעה בהצלחה"
    #     # message = {"message": "התחברות בוצעה בהצלחה"}  # Return message as a dictionary
    #     message = "התחברות בוצעה בהצלחה"  # Return message as a string
    #      # Add debug prints before the return
    #     print(f"user_id: {user_id}")
    #     print(f"message: {message}")
    #     print(f"user_firstName: {user_firstName}")
    #     print(f"user_lastName: {user_lastName}")

    #     return user_firstName, user_lastName, user_id,  message  # Return user_id and message

    def login(self, email, password):
        """Authenticate the user by checking the email and password."""
        try:
            # Check if the email exists in the system
            #user = self.users_byEmail.get(email)  # Use .get() to avoid KeyError

            user = self.getUser_by_email(email)
            if user is None:
                raise UserOrPasswordIncorrectError()

            match_password = self.verify_password(password, user.password)
            # Check if the password matches
            if not match_password:
                raise UserOrPasswordIncorrectError()

            user_id = user.get_user_id()
            user_first_name = user.get_first_name()
            user_last_name = user.get_last_name()
            user.login()
            logging.info(f"Login successful for user: {email}")

            # Debug prints before return
            print(f"user_id: {user_id}")
            print(f"message: {'התחברות בוצעה בהצלחה'}")
            print(f"user_firstName: {user_first_name}")
            print(f"user_lastName: {user_last_name}")

            return user_first_name, user_last_name, user_id, "התחברות בוצעה בהצלחה"

        except UserOrPasswordIncorrectError:
            # Log the error
            print(f"Login failed: Incorrect email or password for {email}")
            return None, None, None, "אימייל או סיסמה שגויים. אנא נסה שוב."

    def logout(self, user_id):
        # Check if the user exists
        user = self.getUser_by_id(user_id)
        if user is None:
            raise UserOrPasswordIncorrectError()
        if not user.loggedIn:
            raise UserIsNotLoggedInError(user_id)
        user.logout()
        
        logging.info(f"User {user_id} logged out successfully.")
        message = "התנתקות בוצעה בהצלחה"
        return message

    def get_user_courses(self, user_id):
        curr_user = self.getUser_by_id(user_id=user_id)
        if curr_user is None:
            return []
        return curr_user.get_courses()

    def registerToCourse(self, courseId, userId):
        """Add user to course (through User object)."""
        user = self.getUser_by_id(userId)
        if user:
            user.registerToCourse(courseId)
        else:
            raise UserDoesnotExistsError(userId)
        
    def editUserProfile(self, email, **kwargs):
        """Edit the user's profile details."""
        user = self.getUser_by_email(email)
        if user:
            user.editProfile(**kwargs)
            return "Profile updated successfully"
        else:
            raise UserDoesnotExistsError()

    def getUser_by_id(self, user_id):
        with self.id_lock:
            user = self.users_byId.get(user_id)
            if user is not None:
                return user
            user_repo = UserRepository()
            user = user_repo.get_user_by_id(user_id=user_id)
            if user:
                self.users_byId[user_id] = user
            return user

    def getUser_by_email(self, email):
        with self.email_lock:
            user = self.users_byEmail.get(email)
            if user is not None:
                return user
            user_repo = UserRepository()
            user = user_repo.get_user_by_email(email=email)
            if user:
                self.users_byEmail[email] = user
            return user

    def registerWithoutAuth(self, email, password, first_name, last_name):
        """
        Unified register function.
        - Sends an authentication code.
        - Verifies the code interactively.
        - Completes the registration.
        """
        if self.getUser_by_email(email) is not None:
            raise Exception("המשתמש כבר קיים במערכת.")

        if not self.is_valid_name(first_name):
            raise Exception("השם הפרטי אינו תקין.")

        if not self.is_valid_name(last_name):
            raise Exception("שם המשפחה אינו תקין.")

        if not self.is_valid_email(email):
            raise Exception("האימייל אינו תקין.")

        if not self.is_valid_password(password):
            raise Exception("הסיסמה אינה תקינה.")

        encrypted_password = self.hash_password(password)

        user_id = self.generateUserId()
        user = User.create(user_id, email, encrypted_password, first_name, last_name)
        #user.login()
        self.users_byEmail[email] = user
        self.users_byId[user_id] = user
        logging.info(f"User {first_name} {last_name} registered successfully.")
        return user_id, {"message": f"User {first_name} {last_name} registered successfully."}





