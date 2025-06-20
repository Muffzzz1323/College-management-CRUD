import streamlit as st
import pandas as pd
import re
import sqlite3
import hashlib
import os
from students import *
from faculty import *
from courses import *
from enrollments import *

# --- CLOUD DATABASE CONNECTION ---
def create_connection():
    db_url = os.getenv("DATABASE_URL", "college.db")
    return sqlite3.connect(db_url, check_same_thread=False)

st.set_page_config(
    page_title="College Management System",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug': 'https://github.com/your-org/your-repo/issues',
        'About': 'College Management System using Python, SQLite and Streamlit.'
    }
)

# --- PASSWORD HASHING ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    return hash_password(password) == hashed

# --- SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'role' not in st.session_state:
    st.session_state.role = ''

# --- USER MANAGEMENT ---
def validate_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", [
            ('admin', hash_password('admin123'), 'admin'),
            ('staff', hash_password('staff123'), 'staff')
        ])
        conn.commit()
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result and check_password(password, result[0]):
        return result[1]
    return None

def register_user():
    st.subheader("Register New User")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    new_role = st.selectbox("Role", ["admin", "staff"])
    if st.button("Register", key="register_btn"):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (new_user,))
        if cursor.fetchone():
            st.error("Username already exists.")
        else:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (new_user, hash_password(new_pass), new_role))
            conn.commit()
            conn.close()
            st.success("User registered successfully.")

# --- LOGIN FUNCTION ---
def login():
    st.markdown('<div class="login-title">Login - College Management System</div>', unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login", key="login_btn"):
        role = validate_user(username, password)
        if role:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.success(f"Welcome, {username.capitalize()}! Role: {role.capitalize()}")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")
    st.markdown("---")
    with st.expander("New user? Register here"):
        register_user()

# --- LOGOUT FUNCTION ---
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ''
    st.session_state.role = ''
    st.success("Logged out successfully.")
    st.experimental_rerun()

# --- ACCESS GATE ---
if not st.session_state.logged_in:
    login()
    st.stop()

# --- PROFESSIONAL THEME ---
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
            margin-top: 20px;
        }
        .login-title {
            font-size: 30px;
            font-weight: 600;
            color: #34495e;
            margin-top: 40px;
            text-align: center;
        }
        .sub-header {
            font-size: 24px;
            color: #16a085;
            padding-top: 15px;
        }
        .stButton>button {
            background: linear-gradient(to right, #0066cc, #3399ff);
            color: white;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            margin-top: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(to right, #004c99, #1a8cff);
        }
        .stTextInput>div>div>input {
            border-radius: 6px;
            padding: 8px;
        }
        .stSelectbox>div>div {
            border-radius: 6px;
        }
        @media screen and (max-width: 768px) {
            .main-title {
                font-size: 28px;
            }
            .sub-header {
                font-size: 20px;
            }
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">College Management System Dashboard</div>', unsafe_allow_html=True)

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/201/201818.png", width=80)
st.sidebar.markdown(f"**Logged in as:** {st.session_state.username} ({st.session_state.role})")
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", ["Students", "Faculty", "Courses", "Enrollments", "Dashboard"])
st.sidebar.button("Logout", on_click=logout)

# --- FORM LEVEL ACCESS CONTROL (example usage) ---
if st.session_state.role != "admin":
    st.warning("Some features are restricted to admin users only.")
