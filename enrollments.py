import streamlit as st
import sqlite3
import pandas as pd

# --- DB CONNECTION ---
def create_connection():
    return sqlite3.connect("college.db", check_same_thread=False)

# --- MAIN UI ---
def manage_enrollments():
    st.subheader("Enrollment Management")
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            course_id TEXT
        )
    """)

    st.markdown("### Enroll Student in Course")
    students = pd.read_sql("SELECT student_id FROM students", conn)["student_id"].tolist()
    courses = pd.read_sql("SELECT course_id FROM courses", conn)["course_id"].tolist()

    with st.form("enroll_form"):
        sid = st.selectbox("Select Student ID", students)
        cid = st.selectbox("Select Course ID", courses)
        submit = st.form_submit_button("Enroll")

        if submit:
            cursor.execute("SELECT * FROM enrollments WHERE student_id=? AND course_id=?", (sid, cid))
            if cursor.fetchone():
                st.warning("This enrollment already exists.")
            else:
                cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (sid, cid))
                conn.commit()
                st.success("Enrollment added successfully.")

    st.markdown("---")
    st.markdown("### View Enrollments")
    df = pd.read_sql("SELECT * FROM enrollments", conn)
    st.dataframe(df, use_container_width=True)

    if st.session_state.role == "admin":
        st.markdown("### Delete Enrollment")
        enrollment_id = st.number_input("Enter Enrollment ID to delete", min_value=1)
        if st.button("Delete"):
            cursor.execute("DELETE FROM enrollments WHERE id=?", (enrollment_id,))
            conn.commit()
            st.success("Deleted if existed.")
    else:
        st.info("Only admin can delete enrollments.")

    conn.close()

