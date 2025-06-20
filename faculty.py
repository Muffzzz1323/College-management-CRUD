from database import create_connection

def add_faculty(faculty_id, name, department, email):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS faculty (faculty_id TEXT PRIMARY KEY, name TEXT, department TEXT, email TEXT)")
        cursor.execute("INSERT INTO faculty VALUES (?, ?, ?, ?)", (faculty_id, name, department, email))
        conn.commit()
        print("✅ Faculty added.")
    except:
        print("❌ Faculty already exists.")
    conn.close()

def view_faculty():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faculty")
    for row in cursor.fetchall():
        print(row)
    conn.close()

def update_faculty_email(faculty_id, new_email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE faculty SET email = ? WHERE faculty_id = ?", (new_email, faculty_id))
    conn.commit()
    print("✏️ Faculty email updated.")
    conn.close()

def delete_faculty(faculty_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM faculty WHERE faculty_id = ?", (faculty_id,))
    conn.commit()
    print("🗑️ Faculty deleted.")
    conn.close()
