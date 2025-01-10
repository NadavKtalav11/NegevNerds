NegevNerds
NegevNerds is a collaborative web-based platform designed to help university students share and interact with exam-related resources.
 The platform enables users to post exam questions, participate in discussions, and provide feedback through reactions and comments. 
It aims to foster a community-driven environment for academic success.

Features
Exam Questions Repository:

Users can upload exam questions with details such as year, semester, moed.
Comment and Reaction System:

Comments can be added to questions to facilitate discussions.
Reactions (using emojis) allow users to quickly provide feedback on comments.
Topic and Tag Management:

Questions and courses are categorized by topics to make searching and browsing easier.
Questions are linked to specific topics for better organization.
Course Management:

Courses are managed by designated managers who oversee uploaded content.
Students can associate themselves with courses to receive tailored notifications and updates.
User Notifications:

The platform sends notifications for updates, comments, and approvals, ensuring users stay informed.
Language Support:

Supports English and Hebrew letter-specific models to handle a multilingual user base effectively.
Technology Stack
Backend: Python, Flask, SQLAlchemy

The backend handles data persistence, business logic, and communication with the database.
Key models include:
UserModel, CourseModel, ExamModel, CommentModel, ReactionModel, and more.
Custom models dynamically generated for English and Hebrew alphabet-based tables.

Frontend: React.js

Provides an intuitive user interface for seamless interaction.
Components include forms for question submission, discussion threads, and notifications.

Database:

Relational database for storing structured data (e.g., user profiles, courses, exams, comments).
Relationships are managed using SQLAlchemy ORM.
Key Models and Relationships
User Management:


How to Run the Project
Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/negev-nerds.git
cd negev-nerds
Backend Setup:

Install required Python packages:
bash
Copy code
pip install -r requirements.txt
Run the backend server:
bash
Copy code
python app.py
Frontend Setup:

Navigate to the ReactNN directory:
bash
Copy code
cd ReactNN
Install dependencies:
bash
Copy code
npm install
Run the frontend:
bash
Copy code
npm start
Access the Application: Open your browser and go to http://localhost:3000.

Contributing
We welcome contributions to NegevNerds! Please follow these steps:

Fork the repository.
Create a new branch:
bash
Copy code
git checkout -b feature-name
Commit your changes and push to your fork.
Open a pull request with a detailed description of your changes.
