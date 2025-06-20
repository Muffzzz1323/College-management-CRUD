import streamlit as st
from database import initialize_db
from students import manage_students
from faculty import manage_faculty
from courses import manage_courses
from enrollments import manage_enrollments
import sqlite3
import hashlib

# --- INITIALIZE DB TABLES ---
initialize_db()

# --- SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'role' not in st.session_state:
    st.session_state.role = ''

# --- AUTHENTICATION ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] == hash_password(password):
        return result[1]
    return None

def register_user():
    st.subheader("Register")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    role = st.selectbox("Role", ["admin", "staff"])
    if st.button("Register"):
        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (new_user,))
        if cursor.fetchone():
            st.warning("Username already exists.")
        else:
            cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (new_user, hash_password(new_pass), role))
            conn.commit()
            conn.close()
            st.success("User registered successfully.")

def login():
    st.markdown("<div class='login-title'>Login to College Management System</div>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        role = check_credentials(username, password)
        if role:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.success(f"Welcome, {username} ({role})")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

    with st.expander("New user? Register here"):
        register_user()

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ''
    st.session_state.role = ''
    st.experimental_rerun()

# --- CSS STYLES ---
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
        }
        .main-title {
            font-size: 36px;
            font-weight: 700;
            color: #2c3e50;
            text-align: center;
        }
        .login-title {
            font-size: 28px;
            font-weight: 600;
            color: #34495e;
            text-align: center;
            margin-top: 30px;
        }
        .stButton>button {
            background: linear-gradient(to right, #0066cc, #3399ff);
            color: white;
            font-weight: 600;
            border-radius: 8px;
            padding: 10px 20px;
            margin-top: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stButton>button:hover {
            background: linear-gradient(to right, #004c99, #1a8cff);
        }
        .sub-header {
            font-size: 22px;
            color: #2980b9;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# --- GATE ---
if not st.session_state.logged_in:
    login()
    st.stop()

# --- MAIN APP ---
st.markdown('<div class="main-title">College Management System</div>', unsafe_allow_html=True)

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", ["Students", "Faculty", "Courses", "Enrollments"])
if st.sidebar.button("Logout"):
    logout()

if menu == "Students":
    manage_students()
elif menu == "Faculty":
    manage_faculty()
elif menu == "Courses":
    manage_courses()
elif menu == "Enrollments":
    manage_enrollments()
