
# Quiz Application

A Flask-based multi-user quiz application that allows administrators to create and manage quizzes while users can take quizzes and track their scores.

## Features

- User Authentication (Login/Register)
- Admin Dashboard
  - Manage Subjects
  - Manage Chapters
  - Manage Quizzes
  - Manage Questions
  - View All Users' Scores
- User Features
  - Take Quizzes
  - View Personal Scores
  - Track Progress

## Tech Stack

- Python 3.11+
- Flask
- SQLAlchemy
- Flask-Login
- SQLite Database

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python app.py
```

## Default Admin Login

- Username: admin
- Password: admin

## Project Structure

```
├── static/
│   └── styles.css
├── templates/
│   ├── admin_dashboard.html
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── quiz.html
│   ├── register.html
│   └── scores.html
├── app.py
├── config.py
├── database.py
├── models.py
└── requirements.txt
```

## Database Models

- User: Stores user information and authentication details
- Subject: Main categories for quizzes
- Chapter: Subcategories under subjects
- Quiz: Collection of questions
- Question: Individual questions with options
- Score: Tracks user quiz attempts and scores

## License

MIT License
