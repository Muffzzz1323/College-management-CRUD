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

def faculty_exists(faculty_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faculty WHERE faculty_id=?", (faculty_id,))
    return cursor.fetchone() is not None

# --- MAIN UI ---
def manage_faculty():
    st.subheader("Faculty Management")
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faculty (
            faculty_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            experience INTEGER NOT NULL
        )
    """)

    with st.form("add_faculty_form"):
        st.markdown("### Add New Faculty")
        fid = st.text_input("Faculty ID")
        name = st.text_input("Name")
        dept = st.text_input("Department")
        exp = st.number_input("Experience (years)", min_value=0, max_value=50)
        submit = st.form_submit_button("Add Faculty")

        if submit:
            if not (fid and name and dept):
                st.error("All fields are required.")
            elif not is_valid_name(name):
                st.error("Invalid name. Use alphabetic characters only.")
            elif faculty_exists(fid):
                st.warning("Faculty with this ID already exists.")
            else:
                cursor.execute("INSERT INTO faculty VALUES (?, ?, ?, ?)", (fid, name, dept, exp))
                conn.commit()
                st.success("Faculty added successfully.")

    st.markdown("---")
    st.markdown("### View Faculty Members")
    df = pd.read_sql("SELECT * FROM faculty", conn)
    st.dataframe(df, use_container_width=True)

    if st.session_state.role == "admin":
        st.markdown("### Delete Faculty")
        faculty_to_delete = st.text_input("Enter Faculty ID to delete")
        if st.button("Delete"):
            cursor.execute("DELETE FROM faculty WHERE faculty_id=?", (faculty_to_delete,))
            conn.commit()
            st.success("Deleted if existed.")
    else:
        st.info("Only admin can delete faculty.")

    conn.close()

