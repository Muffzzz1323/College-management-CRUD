from database import create_connection

def create_courses_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                        course_id TEXT PRIMARY KEY,
                        course_name TEXT NOT NULL,
                        faculty_id TEXT NOT NULL,
                        FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id))''')
    conn.commit()
    conn.close()

def add_course(course_id, course_name, faculty_id):
    create_courses_table()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO courses VALUES (?, ?, ?)", (course_id, course_name, faculty_id))
        conn.commit()
        print("✅ Course added.")
    except Exception as e:
        print("❌ Error:", e)
    conn.close()

def view_courses():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    for row in cursor.fetchall():
        print(row)
    conn.close()

def update_course_name(course_id, new_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE courses SET course_name = ? WHERE course_id = ?", (new_name, course_id))
    conn.commit()
    print("✏️ Course name updated.")
    conn.close()

def delete_course(course_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
    conn.commit()
    print("🗑️ Course deleted.")
    conn.close()
