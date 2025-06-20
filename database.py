import sqlite3

def create_connection():
    return sqlite3.connect("college.db")

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        student_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        department TEXT NOT NULL,
                        year INTEGER,
                        email TEXT UNIQUE)''')

    # Optional: Add more tables here for faculty, courses, enrollments

    conn.commit()
    conn.close()

# Run table creation
if __name__ == "__main__":
    create_tables()
