import unittest
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, timedelta
import sys
import os

from Backend.BusinessLayer.Util.Exceptions import UserOrPasswordIncorrectError, UserIsNotLoggedInError

# Add Backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from Backend.BusinessLayer.User.UserFacade import UserFacade
from Backend.BusinessLayer.User.User import *


class TestUserController(unittest.TestCase):
    def setUp(self):
        """Set up a fresh UserController instance for each test."""
        self.user_controller = UserFacade()
        # self.addCleanup(patch.stopall)
        self.mock_user = MagicMock()
        self.mock_user.logout = MagicMock()

    # @patch("builtins.input", side_effect=["123456", "כן"])  # Mock user inputs for auth code and terms acceptance
    # @patch("BusinessLayer.User.UserController.UserController.send_auth_code")  # Mock send_auth_code
    # @patch("builtins.open", new_callable=mock_open, read_data="Mock Terms of Use")  # Mock file read
    # def test_register_valid_email_password(self, mock_open_file, mock_send_auth_code, mock_input):
    #     """Test registration with valid email and password."""
    #     # Mock send_auth_code to simulate email sending
    #     mock_send_auth_code.return_value = None

    #     # Set up a pending authentication code for the test email
    #     email = "testuser@post.bgu.ac.il"
    #     self.user_controller.pending_auth_codes[email] = (123456, datetime.now() + timedelta(minutes=3))

    #     # Call the register function
    #     result = self.user_controller.register(
    #         email=email,
    #         password="Valid12!",
    #         first_name="Test",
    #         last_name="User"
    #     )

    #     # Assertions
    #     self.assertIn(email, self.user_controller.users)  # User should be in the system
    #     self.assertEqual(self.user_controller.users[email].first_name, "Test")  # First name should match
    #     self.assertEqual(self.user_controller.users[email].last_name, "User")  # Last name should match
    #     self.assertEqual(self.user_controller.users[email].password, "Valid12!")  # Password should match
    #     self.assertEqual(result["message"], "User Test User registered successfully.")  # Success message

    # def test_register_multiple_invalid_emails(self):
    #     """Test multiple users trying to register with invalid emails."""
    #     invalid_emails = [
    #         "user1@gmail.com",  # Invalid domain
    #         "user2@yahoo.com",  # Invalid domain
    #         "user3@",           # Missing domain part
    #         "@bgu.ac.il",       # Missing local part
    #         "user4.bgu.ac.il",  # Missing '@'
    #     ]
        
    #     for email in invalid_emails:
    #         with self.subTest(email=email):
    #             with self.assertRaises(Exception) as context:
    #                 self.user_controller.register(
    #                     email=email,
    #                     password="Valid12!",  # Valid password
    #                     first_name="Test",
    #                     last_name="User"
    #                 )
    #             # Check the exception message
    #             self.assertEqual(str(context.exception), "Invalid email")
    
    # def test_register_invalid_passwords(self):
    #     """Test registration with invalid passwords."""
    #     # Mock the send_auth_code to avoid actually sending an email

    #     invalid_passwords = [
    #         "short",          # Less than 8 characters
    #         "onlylowercase",  # No uppercase letter
    #         "ONLYUPPERCASE",  # No lowercase letter
    #         "NoNum!ber",       # No number
    #         "1234@5678",       # No letter
    #         "NoSpecialChar1", # No special character
    #         "!@#$%^&*",       # No letter or number
    #     ]

    #     email = "testuser@post.bgu.ac.il"

    #     for password in invalid_passwords:
    #         with self.assertRaises(Exception) as context:
    #             self.user_controller.register(
    #                 email=email,
    #                 password=password,
    #                 first_name="Test",
    #                 last_name="User"
    #             )
    #         self.assertEqual(str(context.exception), "Invalid password")


    # @patch("builtins.open", new_callable=mock_open, read_data="Mock Terms of Use")  # Mock terms of use file
    # @patch("builtins.input", side_effect=["123456", "כן"])  # Mock user input for auth code and terms acceptance
    # @patch("BusinessLayer.User.UserController.UserController.send_auth_code")  # Mock send_auth_code
    # def test_register_duplicate_email(self, mock_send_auth_code, mock_input, mock_open_file):
    #     """Test registering the same email twice, with Terms of Use mocked."""
    #     # Mock the send_auth_code to avoid actually sending an email
    #     mock_send_auth_code.return_value = None  # send_auth_code has no return value

    #     self.assertEqual(0, len(self.user_controller.users))
    #     # Mocked authentication code and expiry
    #     email = "testuser@post.bgu.ac.il"
    #     self.user_controller.pending_auth_codes[email] = (123456, datetime.now() + timedelta(minutes=3))

    #     # First registration should succeed
    #     result = self.user_controller.register(
    #         email=email,
    #         password="ValidPassword1!",
    #         first_name="Test",
    #         last_name="User"
    #     )

    #     # Assert the user was registered successfully
    #     self.assertIn(email, self.user_controller.users)  # User should be added
    #     self.assertEqual(result["message"], "User Test User registered successfully.")
    #     self.assertEqual(1, len(self.user_controller.users))

    #     # Attempt to register the same email again, expecting an exception
    #     with self.assertRaises(Exception) as context:
    #         self.user_controller.register(
    #             email=email,
    #             password="ValidPassword1!",
    #             first_name="Test",
    #             last_name="User"
    #         )

    #     # Assert that the exception message is correct and the number of users is unchanged
    #     self.assertEqual(str(context.exception), "User already exists.")
    #     self.assertEqual(1, len(self.user_controller.users))


    # @patch("builtins.open", new_callable=mock_open, read_data="Mock Terms of Use")  # Mock terms of use file
    # @patch("builtins.input", side_effect=["123456", "כן"])  # Mock user input for auth code and terms acceptance
    # @patch("BusinessLayer.User.UserController.UserController.send_auth_code")  # Mock send_auth_code
    # def test_register_with_automatic_login(self, mock_send_auth_code, mock_input, mock_open_file):
    #     """Test that a user is automatically logged in upon successful registration."""
    #     # Mock the send_auth_code to avoid actually sending an email
    #     mock_send_auth_code.return_value = None

    #     # Mocked authentication code and expiry
    #     email = "testuser@post.bgu.ac.il"
    #     self.user_controller.pending_auth_codes[email] = (123456, datetime.now() + timedelta(minutes=3))

    #     # Call the register function
    #     result = self.user_controller.register(
    #         email=email,
    #         password="ValidPassword1!",
    #         first_name="Test",
    #         last_name="User"
    #     )

    #     # Assertions
    #     self.assertIn(email, self.user_controller.users)  # User should be added
    #     user = self.user_controller.users[email]
    #     self.assertTrue(user.loggedIn)  # User should be logged in
    #     self.assertEqual(result["message"], "User Test User registered successfully.")

    @patch("builtins.open", new_callable=mock_open, read_data="Mock Terms of Use")  # Mock terms of use file
    @patch("builtins.input", side_effect=["123456", "כן"])  # Mock user input for auth code and terms acceptance
    @patch("Backend.BusinessLayer.User.UserFacade.UserFacade.send_auth_code")  # Mock send_auth_code
    def test_register_with_automatic_login(self, mock_send_auth_code, mock_input, mock_open_file):
        """Test that a user is automatically logged in upon successful registration."""
        # Mock send_auth_code to simulate email sending and adding auth code to pending_auth_codes
        def mock_send_auth_code_side_effect(email, first_name):
            auth_code = 123456
            expiry = datetime.now() + timedelta(minutes=3)
            self.user_controller.pending_auth_codes[email] = (auth_code, expiry)
        
        mock_send_auth_code.side_effect = mock_send_auth_code_side_effect

        # Step 1: Call register to send the auth code
        email = "testuser@post.bgu.ac.il"
        password = "ValidPassword1!"
        first_name = "Test"
        last_name = "User"
        
        result_step1 = self.user_controller.register(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Assertions for step 1
        self.assertEqual(result_step1["message"], f"קוד אימות נשלח למייל {email}")
        self.assertIn(email, self.user_controller.pending_auth_codes)  # Ensure auth code was created

        # Simulate calling register2 to complete the registration
        result_step2 = self.user_controller.register_authentication_part(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            auth_code=123456
        )

        # Assertions for step 2
        self.assertIn(email, self.user_controller.users_byEmail)  # User should be added
        user = self.user_controller.users_byEmail[email]
        self.assertTrue(user.loggedIn)  # User should be logged in
        self.assertEqual(result_step2["message"], "User Test User registered successfully.")

    def test_login_successful(self):
        """Test successful login with correct email and password."""
        # Add a test user to the system
        email = "testuser@post.bgu.ac.il"
        password = "ValidPassword1!"
        first_name = "Test"
        last_name = "User"
        user_id = self.user_controller.generateUserId()
        user = User(user_id, email, password, first_name, last_name)
        self.user_controller.users_byEmail[email] = user

        self.assertFalse(user.loggedIn)  # User should not be logged in

        # Perform login
        result = self.user_controller.login(email, password)
        message = "התחברות בוצעה בהצלחה"

        # Assertions
        self.assertTrue(user.loggedIn)  # User should be logged in
        self.assertEqual(result, message)

    def test_login_failure_invalid_email(self):
        """Test login failure with an invalid email."""
        # Attempt to log in with a non-existing email
        message = f"אימייל או סיסמה שגויים. אנא נסה שוב."
        with self.assertRaises(UserOrPasswordIncorrectError) as context:
            self.user_controller.login("invalid@post.bgu.ac.il", "ValidPassword1!")
        self.assertEqual(str(context.exception), message)

    def test_login_failure_invalid_password(self):
        """Test login failure with an invalid password."""
        # Add a test user to the system
        email = "testuser@post.bgu.ac.il"
        password = "ValidPassword1!"
        first_name = "Test"
        last_name = "User"
        user_id = self.user_controller.generateUserId()
        user = User(user_id, email, password, first_name, last_name)
        self.user_controller.users_byEmail[email] = user
        message = f"אימייל או סיסמה שגויים. אנא נסה שוב."
        # Attempt to log in with the wrong password
        with self.assertRaises(UserOrPasswordIncorrectError) as context:
            self.user_controller.login(email, "WrongPassword!")
        self.assertEqual(str(context.exception), message)

    def test_logout_success(self):
        """Test successful logout of an existing user."""
        email = "testuser@post.bgu.ac.il"
        password = "ValidPassword1!"
        first_name = "Test"
        last_name = "User"
        user_id = self.user_controller.generateUserId()
        user = User(user_id, email, password, first_name, last_name)
        self.user_controller.users_byEmail[email] = user
        user.login()
        self.assertTrue(user.loggedIn)  # User shoult be logged in

        result = self.user_controller.logout(email)
        # Assertions
        message = "התנתקות בוצעה בהצלחה"
        self.assertFalse(user.loggedIn)  # User should be logged in
        self.assertEqual(result,message)

    def test_logout_user_does_not_exist(self):
        # Attempt to log in with a non-existing email
        email = "inval555id@post.bgu.ac.il"
        message = f"אימייל או סיסמה שגויים. אנא נסה שוב."

        with self.assertRaises(UserOrPasswordIncorrectError) as context:
            self.user_controller.logout(email)
        self.assertEqual(str(context.exception), message)
   
    def test_logOut_not_loggedIn_user(self):
        email = "testuser@post.bgu.ac.il"
        password = "ValidPassword1!"
        first_name = "Test"
        last_name = "User"
        user_id = self.user_controller.generateUserId()
        user = User(user_id, email, password, first_name, last_name)
        self.user_controller.users_byEmail[email] = user
        self.assertFalse(user.loggedIn)  # User shoult not be logged in
        message = f"לא ניתן להתנתק {email} מכיוון שהוא אינו מחובר."

        with self.assertRaises(UserIsNotLoggedInError) as context:
            self.user_controller.logout(email)
        self.assertEqual(str(context.exception), message)


if __name__ == "__main__":
    unittest.main()
