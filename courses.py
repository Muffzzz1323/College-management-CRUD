import streamlit as st
import sqlite3
import pandas as pd

# --- DB CONNECTION ---
def create_connection():
    return sqlite3.connect("college.db", check_same_thread=False)

def course_exists(course_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses WHERE course_id=?", (course_id,))
    return cursor.fetchone() is not None

# --- MAIN UI ---
def manage_courses():
    st.subheader("Course Management")
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY,
            course_name TEXT NOT NULL,
            department TEXT NOT NULL,
            credits INTEGER NOT NULL
        )
    """)

    with st.form("add_course_form"):
        st.markdown("### Add New Course")
        cid = st.text_input("Course ID")
        cname = st.text_input("Course Name")
        dept = st.text_input("Department")
        credits = st.number_input("Credits", min_value=1, max_value=6)
        submit = st.form_submit_button("Add Course")

        if submit:
            if not (cid and cname and dept):
                st.error("All fields are required.")
            elif course_exists(cid):
                st.warning("Course with this ID already exists.")
            else:
                cursor.execute("INSERT INTO courses VALUES (?, ?, ?, ?)", (cid, cname, dept, credits))
                conn.commit()
                st.success("Course added successfully.")

    st.markdown("---")
    st.markdown("### View Courses")
    df = pd.read_sql("SELECT * FROM courses", conn)
    st.dataframe(df, use_container_width=True)

    if st.session_state.role == "admin":
        st.markdown("### Delete Course")
        course_to_delete = st.text_input("Enter Course ID to delete")
        if st.button("Delete"):
            cursor.execute("DELETE FROM courses WHERE course_id=?", (course_to_delete,))
            conn.commit()
            st.success("Deleted if existed.")
    else:
        st.info("Only admin can delete courses.")

    conn.close()

