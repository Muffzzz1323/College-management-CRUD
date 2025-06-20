College Management System - CRUD Application

This is a complete College Management System built using Python, SQLite, and Streamlit. It provides a clean, interactive interface for managing Students, Faculty, Courses, and Enrollments, with full Create, Read, Update, and Delete (CRUD) functionalities. The project is ideal for demonstrating database-driven application development with a responsive web-based interface.

Features

- Student Management: Add, view, update, and delete student records.
- Faculty Management: Maintain and update faculty details.
- Course Management: Create courses and manage course-related data.
- Enrollment Management: Enroll students into courses and manage their enrollment information.
- Input Validation: Validates user inputs across all modules.
- Streamlit UI: User-friendly, organized, and responsive interface.
- Local Database: Uses SQLite (`college.db`) for fast and reliable data storage.

Technologies Used

| Technology | Description                      |
|------------|----------------------------------|
| Python     | Core language for logic and UI   |
| SQLite     | Lightweight relational database  |
| Streamlit  | Web interface for Python apps    |
| pandas     | Data display and table handling  |

Project Structure

college-management/
│
├── students.py # Student management module
├── faculty.py # Faculty management module
├── courses.py # Course management module
├── enrollments.py # Enrollment handling module
├── database.py # SQLite CRUD operations
├── ui_streamlit.py # Main Streamlit application
├── college.db # SQLite database file
├── requirements.txt # Python dependencies
└── README.md # Project documentation


Setup Instructions

1. Clone the Repository:
   git clone https://github.com/yourusername/college-management.git
   cd college-management
2.Create and Activate a Virtual Environment (Optional but Recommended):
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3.Install the Required Packages:
    pip install -r requirements.txt

4.Run the Streamlit Application
    streamlit run ui_streamlit.py:
    
Future Enhancements
    Authentication and role-based access control
    Exporting data to Excel/CSV
    Admin dashboard with analytics
    Search and filter features in data tables
    Option to connect with a cloud-based database

License
This project is open source and available under the MIT License.

Author
Balkis Bee
Email: balkisbee9@gmail.com
LinkedIn: linkedin.com/in/balkisbee
