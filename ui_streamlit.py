import streamlit as st
import pandas as pd
from students import *
from faculty import *
from courses import *
from enrollments import *
from database import create_connection

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="🎓 College Management System",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- STYLING ----
st.markdown("""
    <style>
        .main-title {
            font-size: 42px;
            font-weight: 700;
            color: #3f51b5;
            text-align: center;
            padding-bottom: 10px;
        }
        .sub-header {
            font-size: 26px;
            color: #009688;
            padding-top: 20px;
        }
        .stButton>button {
            background-color: #009688;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5em 1em;
        }
    </style>
""", unsafe_allow_html=True)

# ---- MAIN TITLE ----
st.markdown('<div class="main-title">College Management System Dashboard</div>', unsafe_allow_html=True)

# ---- SIDEBAR ----
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/201/201818.png", width=100)
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", ["Students", "Faculty", "Courses", "Enrollments", "Dashboard"])

# ---- STUDENTS MODULE ----
if menu == "Students":
    st.markdown("<div class='sub-header'>👨‍🎓 Student Management</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["➕ Add Student", "📋 View/Search Students"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            sid = st.number_input("Student ID", min_value=1)
            name = st.text_input("Full Name")
            dept = st.selectbox("Department", ["CSE", "ECE", "EEE", "MECH", "CIVIL"])
        with col2:
            year = st.selectbox("Year", [1, 2, 3, 4])
            email = st.text_input("Email")
        if st.button("Add Student"):
            add_student(sid, name, dept, year, email)
            st.success("✅ Student added successfully")

    with tab2:
        df = pd.DataFrame(view_students(), columns=["ID", "Name", "Dept", "Year", "Email"])
        search_term = st.text_input("Search by Name")
        if search_term:
            df = df[df["Name"].str.contains(search_term, case=False)]
        st.dataframe(df, use_container_width=True)
        st.download_button("⬇️ Export as CSV", data=df.to_csv(index=False), file_name="students.csv")

# ---- FACULTY MODULE ----
elif menu == "Faculty":
    st.markdown("<div class='sub-header'>👩‍🏫 Faculty Management</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["➕ Add Faculty", "📋 View Faculty"])
    with tab1:
        fid = st.text_input("Faculty ID")
        name = st.text_input("Full Name")
        dept = st.selectbox("Department", ["CSE", "ECE", "EEE", "MECH", "CIVIL"])
        email = st.text_input("Email")
        if st.button("Add Faculty"):
            add_faculty(fid, name, dept, email)
            st.success("✅ Faculty added successfully")
    with tab2:
        df = pd.DataFrame(view_faculty(), columns=["ID", "Name", "Dept", "Email"])
        st.dataframe(df, use_container_width=True)
        st.download_button("⬇️ Export as CSV", data=df.to_csv(index=False), file_name="faculty.csv")

# ---- COURSES MODULE ----
elif menu == "Courses":
    st.markdown("<div class='sub-header'>📚 Course Management</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["➕ Add Course", "📋 View Courses"])
    with tab1:
        cid = st.text_input("Course ID")
        cname = st.text_input("Course Name")
        fid = st.text_input("Faculty ID")
        if st.button("Add Course"):
            add_course(cid, cname, fid)
            st.success("✅ Course added successfully")
    with tab2:
        df = pd.DataFrame(view_courses(), columns=["ID", "Name", "Faculty ID"])
        st.dataframe(df, use_container_width=True)
        st.download_button("⬇️ Export as CSV", data=df.to_csv(index=False), file_name="courses.csv")

# ---- ENROLLMENTS MODULE ----
elif menu == "Enrollments":
    st.markdown("<div class='sub-header'>📝 Enrollment Management</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["➕ Enroll Student", "📋 View Enrollments"])
    with tab1:
        student_id = st.number_input("Student ID", min_value=1)
        course_id = st.text_input("Course ID")
        grade = st.selectbox("Grade", ["A", "B", "C", "D", "F"])
        if st.button("Enroll"):
            add_enrollment(student_id, course_id, grade)
            st.success("✅ Enrollment successful")
    with tab2:
        df = pd.DataFrame(view_enrollments(), columns=["Enroll ID", "Student ID", "Course ID", "Grade"])
        st.dataframe(df, use_container_width=True)
        st.download_button("⬇️ Export as CSV", data=df.to_csv(index=False), file_name="enrollments.csv")

# ---- DASHBOARD MODULE ----
elif menu == "Dashboard":
    st.markdown("<div class='sub-header'>📈 Analytics Dashboard</div>", unsafe_allow_html=True)
    conn = create_connection()
    df_students = pd.read_sql("SELECT department, COUNT(*) as count FROM students GROUP BY department", conn)
    df_years = pd.read_sql("SELECT year, COUNT(*) as count FROM students GROUP BY year", conn)
    df_faculty = pd.read_sql("SELECT department, COUNT(*) as count FROM faculty GROUP BY department", conn)
    conn.close()

    col1, col2, col3 = st.columns(3)
    col1.metric("🎓 Total Students", df_students["count"].sum())
    col2.metric("📘 Total Courses", len(view_courses()))
    col3.metric("👩‍🏫 Total Faculty", df_faculty["count"].sum())

    st.markdown("---")
    col4, col5 = st.columns(2)
    with col4:
        st.subheader("📊 Students per Department")
        st.bar_chart(df_students.set_index("department"))
    with col5:
        st.subheader("📊 Students per Year")
        st.bar_chart(df_years.set_index("year"))
