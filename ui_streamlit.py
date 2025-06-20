import streamlit as st
import pandas as pd
from students import *
from faculty import *
from courses import *
from enrollments import *

st.set_page_config(page_title="College Management System", layout="wide")
st.title("🎓 College Management System")

menu = st.sidebar.selectbox("Choose Module", ["Students", "Faculty", "Courses", "Enrollments", "Dashboard"])

# ---------- STUDENTS ----------
if menu == "Students":
    st.header("👩‍🎓 Student Management")
    option = st.radio("Operation", ["Add", "View", "Update Email", "Delete"])

    if option == "Add":
        sid = st.number_input("Student ID", min_value=1)
        name = st.text_input("Name")
        dept = st.text_input("Department")
        year = st.number_input("Year", min_value=1, max_value=4)
        email = st.text_input("Email")
        if st.button("Add Student"):
            add_student(sid, name, dept, year, email)

    elif option == "View":
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(data, columns=["Student ID", "Name", "Department", "Year", "Email"])
        dept_filter = st.text_input("Filter by Department")
        year_filter = st.selectbox("Filter by Year", ["All", 1, 2, 3, 4])
        name_search = st.text_input("Search by Name")

        if dept_filter:
            df = df[df["Department"].str.contains(dept_filter, case=False)]
        if year_filter != "All":
            df = df[df["Year"] == year_filter]
        if name_search:
            df = df[df["Name"].str.contains(name_search, case=False)]

        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download as CSV", csv, "students.csv", "text/csv")

    elif option == "Update Email":
        sid = st.number_input("Student ID", min_value=1)
        new_email = st.text_input("New Email")
        if st.button("Update"):
            update_student_email(sid, new_email)

    elif option == "Delete":
        sid = st.number_input("Student ID", min_value=1)
        if st.button("Delete"):
            delete_student(sid)

# ---------- FACULTY ----------
elif menu == "Faculty":
    st.header("👨‍🏫 Faculty Management")
    option = st.radio("Operation", ["Add", "View", "Update Email", "Delete"])

    if option == "Add":
        fid = st.text_input("Faculty ID")
        name = st.text_input("Name")
        dept = st.text_input("Department")
        email = st.text_input("Email")
        if st.button("Add Faculty"):
            add_faculty(fid, name, dept, email)

    elif option == "View":
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM faculty")
        data = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(data, columns=["Faculty ID", "Name", "Department", "Email"])
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download as CSV", csv, "faculty.csv", "text/csv")

    elif option == "Update Email":
        fid = st.text_input("Faculty ID")
        new_email = st.text_input("New Email")
        if st.button("Update"):
            update_faculty_email(fid, new_email)

    elif option == "Delete":
        fid = st.text_input("Faculty ID")
        if st.button("Delete"):
            delete_faculty(fid)

# ---------- COURSES ----------
elif menu == "Courses":
    st.header("📚 Course Management")
    option = st.radio("Operation", ["Add", "View", "Update Name", "Delete"])

    if option == "Add":
        cid = st.text_input("Course ID")
        name = st.text_input("Course Name")
        fid = st.text_input("Faculty ID")
        if st.button("Add Course"):
            add_course(cid, name, fid)

    elif option == "View":
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses")
        data = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(data, columns=["Course ID", "Course Name", "Faculty ID"])
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download as CSV", csv, "courses.csv", "text/csv")

    elif option == "Update Name":
        cid = st.text_input("Course ID")
        new_name = st.text_input("New Course Name")
        if st.button("Update"):
            update_course_name(cid, new_name)

    elif option == "Delete":
        cid = st.text_input("Course ID")
        if st.button("Delete"):
            delete_course(cid)

# ---------- ENROLLMENTS ----------
elif menu == "Enrollments":
    st.header("📝 Enrollment Management")
    option = st.radio("Operation", ["Add", "View", "Update Grade", "Delete"])

    if option == "Add":
        sid = st.number_input("Student ID", min_value=1)
        cid = st.text_input("Course ID")
        grade = st.text_input("Grade")
        if st.button("Add Enrollment"):
            add_enrollment(sid, cid, grade)

    elif option == "View":
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT enrollment_id, students.name, courses.course_name, grade
                          FROM enrollments
                          JOIN students ON students.student_id = enrollments.student_id
                          JOIN courses ON courses.course_id = enrollments.course_id''')
        data = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(data, columns=["Enrollment ID", "Student Name", "Course Name", "Grade"])
        grade_filter = st.text_input("Filter by Grade")
        course_search = st.text_input("Search by Course")

        if grade_filter:
            df = df[df["Grade"].str.contains(grade_filter, case=False)]
        if course_search:
            df = df[df["Course Name"].str.contains(course_search, case=False)]

        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download as CSV", csv, "enrollments.csv", "text/csv")

    elif option == "Update Grade":
        eid = st.number_input("Enrollment ID", min_value=1)
        grade = st.text_input("New Grade")
        if st.button("Update"):
            update_grade(eid, grade)

    elif option == "Delete":
        eid = st.number_input("Enrollment ID", min_value=1)
        if st.button("Delete"):
            delete_enrollment(eid)

# ---------- DASHBOARD ----------
elif menu == "Dashboard":
    st.header("📊 College Analytics Dashboard")

    # Students per department
    conn = create_connection()
    df_students = pd.read_sql_query("SELECT department, COUNT(*) as count FROM students GROUP BY department", conn)
    df_years = pd.read_sql_query("SELECT year, COUNT(*) as count FROM students GROUP BY year", conn)
    df_faculty = pd.read_sql_query("SELECT department, COUNT(*) as count FROM faculty GROUP BY department", conn)
    conn.close()

    st.subheader("Students per Department")
    st.bar_chart(df_students.set_index("department"))

    st.subheader("Students per Year")
    st.bar_chart(df_years.set_index("year"))

    st.subheader("Faculty Count per Department")
    st.bar_chart(df_faculty.set_index("department"))
