import streamlit as st
import sqlite3
import pandas as pd
import re

# --- DB CONNECTION ---
def create_connection():
    return sqlite3.connect("college.db", check_same_thread=False)

# --- VALIDATION ---
def is_valid_name(name):
    return bool(re.match("^[A-Za-z ]+$", name))

def student_exists(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
    return cursor.fetchone() is not None

# --- MAIN UI ---
def manage_students():
    st.subheader("Student Management")
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    """)

    with st.form("add_student_form"):
        st.markdown("### Add New Student")
        sid = st.text_input("Student ID")
        name = st.text_input("Name")
        dept = st.text_input("Department")
        year = st.selectbox("Year", [1, 2, 3, 4])
        submit = st.form_submit_button("Add Student")

        if submit:
            if not (sid and name and dept):
                st.error("All fields are required.")
            elif not is_valid_name(name):
                st.error("Invalid name. Use alphabetic characters only.")
            elif student_exists(sid):
                st.warning("Student with this ID already exists.")
            else:
                cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?)", (sid, name, dept, year))
                conn.commit()
                st.success("Student added successfully.")

    st.markdown("---")
    st.markdown("### View Students")
    df = pd.read_sql("SELECT * FROM students", conn)
    st.dataframe(df, use_container_width=True)

    if st.session_state.role == "admin":
        st.markdown("### Delete Student")
        student_to_delete = st.text_input("Enter Student ID to delete")
        if st.button("Delete"):
            cursor.execute("DELETE FROM students WHERE student_id=?", (student_to_delete,))
            conn.commit()
            st.success("Deleted if existed.")
    else:
        st.info("Only admin can delete students.")

    conn.close()

