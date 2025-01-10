# Negev Nerds

**Negev Nerds** is a collaborative platform designed for university students to share and discuss exam questions. It serves as a space for students to upload past exams, comment on them, and discuss answers to help each other prepare for upcoming exams. The platform promotes learning by providing an organized, searchable collection of exams and questions.

## Features

- **Post Exam Questions**: Students can upload past exam questions to help others prepare. This functionality includes the ability to add relevant metadata (year, semester, moed).
- **Comment on Questions**: Each exam question has a comment section where students can leave explanations, clarifications, or additional information to help other students understand the question better.
- **Like Reactions**: Students can react to comments using emojis, helping highlight useful or popular responses.
- **Search Functionality**: Users can search for exam questions based on keywords, year, semester, and course name, making it easy to find relevant content.
- **User Management**: Only registered and logged-in users can post, comment, and interact with content.

## Technologies Used

- **Frontend**: 
  - React.js: A JavaScript library for building user interfaces.
  - Redux: A state management library to manage the state of the app.
  - Axios: A promise-based HTTP client for making requests from the frontend to the backend.
  
- **Backend**: 
  - Python with Flask/Django: Backend web framework for building APIs and handling requests.
  - SQLAlchemy: ORM for interacting with the database, managing data models, and running queries.
  
- **Database**: 
  - PostgreSQL/SQLite: Relational databases for storing users, courses, questions, and other related data.

- **Version Control**: 
  - Git: A version control system to track changes and collaborate.
  - GitHub: A cloud repository platform to store and share the project codebase.

## Project Structure

The project is divided into two main sections:

### 1. **NegevNerds (Backend)**

This is the backend application that handles all the business logic, database interactions, and API requests. It is built with Python using Flask/Django. Key components of the backend:
- **Models**: Represent the database schema using SQLAlchemy.
- **Controllers**: Handle API requests, process data, and return responses.
- **Authentication**: Manages user login, registration, and access control.

### 2. **ReactNN (Frontend)**

This is the frontend application built with React.js. It communicates with the backend through API requests and renders the user interface. Key components of the frontend:
- **Components**: Reusable building blocks of the UI, such as buttons, input forms, and lists.
- **Pages**: Represent different views or sections of the app (e.g., Home, Post Exam, My Exams).
- **State Management**: Redux handles the global application state, including user authentication and content display.

## Setup

To set up the project locally:

### Step 1: Clone the Repository

Clone the repository to your local machine using the following command:
```bash
git clone https://github.com/yourusername/NegevNerds.git
```
### Step 2: Install Frontend Dependencies
Navigate to the ReactNN directory and install the necessary dependencies:

```bash
cd NegevNerds/ReactNN
npm install
```
### Step 3: Backend Setup
1. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```
### Step 4: Running the Application
Frontend:
To run the frontend application:

```bash
npm start
```
Backend:
To run the backend application:

```bash
python app.py
```
Now you should be able to access the application at http://localhost:3000 for the frontend and http://localhost:5001 for the backend.
