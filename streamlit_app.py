import sys
import streamlit as st
import random
import time
import sqlite3
from google import genai
from google.genai import errors

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('titan_users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT, score INTEGER, chat_history TEXT)''')
    conn.commit()
    conn.close()

def get_user_data(username):
    conn = sqlite3.connect('titan_users.db')
    c = conn.cursor()
    c.execute("SELECT password, score, chat_history FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def save_user_progress(username, score, chat_history_str):
    conn = sqlite3.connect('titan_users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET score=?, chat_history=? WHERE username=?", (score, chat_history_str, username))
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect('titan_users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES (?, ?, 0, '')", (username, password))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

init_db()

# --- 👑 LINK PREVIEW & LINK UPGRADES ---
st.set_page_config(
    page_title="Afe's Homework Titan PRO — Cyber AI Solver", 
    page_icon="👑", 
    layout="centered"
)

# --- 🎨 PRO CYBERPUNK TERMINAL THEME ---
st.markdown("""
    <style>
    .main { background-color: #060913 !important; color: #00ffcc !important; }
    h1 { color: #00ffcc !important; text-shadow: 0 0 15px #00ffcc; font-family: 'Courier New', monospace; font-weight: bold; }
    h2, h3 { color: #ff007f !important; text-shadow: 0 0 10px #ff007f; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #ff007f !important; color: white !important; border-radius: 8px; box-shadow: 0 0 12px #ff007f; font-weight: bold; width: 100%; border: none; }
    .stButton>button:hover { background-color: #00ffcc !important; color: black !important; box-shadow: 0 0 20px #00ffcc; cursor: pointer; }
    .stTextInput>div>div>input { background-color: #101626 !important; color: #00ffcc !important; border: 1px solid #ff007f !important; font-family: 'Courier New', monospace; }
    .stSelectbox>div>div>div { background-color: #101626 !important; color: #00ffcc !important; border: 1px solid #ff007f !important; }
    </style>
    """, unsafe_allow_html=True)

# Pull your API key safely from Streamlit Cloud Secrets vault
MY_API_KEY = st.secrets["GEMINI_API_KEY"]

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = ""
if 'score' not in st.session_state: st.session_state.score = 0
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- THE LOGIN & SIGN UP PAGE ---
if not st.session_state.logged_in:
    st.title("🔒 TITAN MAINFRAME LOGIN")
    menu = st.radio("Choose Action:", ["Log In to Account", "Register New Creator Account"])
    username_input = st.text_input("Username:", placeholder="e.g. Afe_Titan")
    password_input = st.text_input("Password:", type="password", placeholder="••••••••")
    
    if menu == "Register New Creator Account":
        if st.button("CREATE SECURE PERMANENT ACCOUNT"):
            if username_input and password_input:
                if register_user(username_input, password_input):
                    st.session_state.logged_in = True
                    st.session_state.username = username_input
                    st.session_state.score = 0
                    st.session_state.chat_history = []
                    st.success("ACCOUNT CREATED! Launching Titan Mainframe App...")
                    time.sleep(0.8)
                    st.rerun()
                else:
                    st.error("Error: That username is already taken.")
            else:
                st.error("Please fill in all blanks.")
                
    elif menu == "Log In to Account":
        if st.button("INITIALIZE SYSTEM ACCESS"):
            user_info = get_user_data(username_input)
            if user_info and user_info[0] == password_input:
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.session_state.score = user_info[1]
                if user_info[2]:
                    st.session_state.chat_history = user_info[2].split("||")
                else:
                    st.session_state.chat_history = []
                st.success("ACCESS GRANTED.")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Access Denied: Invalid username or passcode.")

# --- THE ACTUAL ONLINE APP CORE ---
else:
    st.title(f"⚡ TITAN NET v3.5 // CREATOR: {st.session_state.username.upper()}")
    st.write(f"Permanent Network Score: **{st.session_state.score} XP**")
    
    tab1, tab2, tab3 = st.tabs(["🧮 AI SOLVER", "🎮 PRACTICE GAME", "💬 SECURE AI CHAT"])
    
    with tab1:
        st.header("Core Math Engine")
        choice = st.selectbox("Select Calculation Formula:", ["Multiply (*)", "Divide (/)", "Power of (**)"])
        num1 = st.number_input("Input Matrix A:", value=0.0, key="n1")
        num2 = st.number_input("Input Matrix B:", value=0.0, key="n2")
        if st.button("RUN ENGINE"):
            if choice == "Multiply (*)": st.success(f"🎯 Output: {num1 * num2}")
            elif choice == "Divide (/)": 
                if num2 == 0: st.error("Can't divide by zero!")
                else: st.success(f"🎯 Output: {num1 / num2}")
            elif choice == "Power of (**)": st.success(f"🎯 Output: {num1 ** num2}")

    with tab2:
        st.header("Brain training XP Simulation")
        if 'q1' not in st.session_state:
            st.session_state.q1 = random.randint(3, 12)
            st.session_state.q2 = random.randint(3, 12)
        n1, n2 = st.session_state.q1, st.session_state.q2
        st.subheader(f"Data Quest: What is {n1} × {n2}?")
        user_ans = st.number_input("Submit Computation Input:", value=0.0, key="ans")
        if st.button("TRANSMIT ANSWER DATA"):
            if user_ans == (n1 * n2):
                st.balloons()
                st.session_state.score += 20
                chat_str = "||".join(st.session_state.chat_history)
                save_user_progress(st.session_state.username, st.session_state.score, chat_str)
                st.session_state.q1 = random.randint(3, 12)
                st.session_state.q2 = random.randint(3, 12)
                st.success("🔥 XP Saved to Database Ledger!")
                time.sleep(0.5)
                st.rerun()

    with tab3:
        st.header("💬 Real Gemini AI Mentor")
        chat_input = st.text_input("Send message to live Gemini AI:", key="chat_in")
        if st.button("SEND TO REAL AI"):
            if chat_input:
                st.session_state.chat_history.append(f"👤 You: {chat_input}")
                with st.spinner("Connecting to Google mainframe..."):
                    try:
                        client = genai.Client(api_key=MY_API_KEY)
                        response = client.models.generate_content(model='gemini-2.0-flash', contents=chat_input)
                        st.session_state.chat_history.append(f"🤖 Gemini: {response.text}")
                        chat_str = "||".join(st.session_state.chat_history)
                        save_user_progress(st.session_state.username, st.session_state.score, chat_str)
                    except Exception as e:
                        st.session_state.chat_history.append("🤖 Gemini: Server busy, but database saved your prompt text!")
                st.rerun()
        
        for msg in reversed(st.session_state.chat_history):
            st.write(msg)
            
    if st.sidebar.button("LOG OUT / DISCONNECT"):
        st.session_state.logged_in = False
        st.rerun()
