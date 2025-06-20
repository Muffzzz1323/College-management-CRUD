from database import create_connection

def add_student(student_id, name, department, year, email):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?)",
                       (student_id, name, department, year, email))
        conn.commit()
        print("✅ Student added.")
    except:
        print("❌ Student ID or Email already exists.")
    conn.close()

def view_students():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        print(row)
    conn.close()

def update_student_email(student_id, new_email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET email = ? WHERE student_id = ?",
                   (new_email, student_id))
    conn.commit()
    print("✏️ Email updated.")
    conn.close()

def delete_student(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    print("🗑️ Student deleted.")
    conn.close()
