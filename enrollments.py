from database import create_connection

def create_enrollments_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS enrollments (
                        enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER,
                        course_id TEXT,
                        grade TEXT,
                        FOREIGN KEY (student_id) REFERENCES students(student_id),
                        FOREIGN KEY (course_id) REFERENCES courses(course_id))''')
    conn.commit()
    conn.close()

def add_enrollment(student_id, course_id, grade):
    create_enrollments_table()
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO enrollments (student_id, course_id, grade) VALUES (?, ?, ?)",
                       (student_id, course_id, grade))
        conn.commit()
        print("✅ Enrollment added.")
    except Exception as e:
        print("❌ Error:", e)
    conn.close()

def view_enrollments():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT enrollment_id, students.name, courses.course_name, grade
                      FROM enrollments
                      JOIN students ON students.student_id = enrollments.student_id
                      JOIN courses ON courses.course_id = enrollments.course_id''')
    for row in cursor.fetchall():
        print(row)
    conn.close()

def update_grade(enrollment_id, new_grade):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE enrollments SET grade = ? WHERE enrollment_id = ?", (new_grade, enrollment_id))
    conn.commit()
    print("✏️ Grade updated.")
    conn.close()

def delete_enrollment(enrollment_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enrollments WHERE enrollment_id = ?", (enrollment_id,))
    conn.commit()
    print("🗑️ Enrollment deleted.")
    conn.close()
