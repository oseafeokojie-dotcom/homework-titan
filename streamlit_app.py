import streamlit as st
from google import genai

# 1. Page Configuration
st.set_page_config(page_title="Afe's Homework Titan", page_icon="🧮", layout="centered")

# 2. 🔑 Safe Keys from Secrets
CORRECT_KEY = st.secrets["DOWNLOAD_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Initialize session states for tracking free usage and chat history
if "free_chat_count" not in st.session_state:
    st.session_state.free_chat_count = 0
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am the Titan Math AI. Ask me any math question!"}
    ]

# 3. Sidebar Configuration (The Store Front)
st.sidebar.title("👑 Homework Titan Store")
st.sidebar.markdown("[👉 CLICK HERE TO BUY PRO KEY (2,500 NGN) 👈](https://selar.com)")
st.sidebar.write("---")

# Key input field
user_key = st.sidebar.text_input("🔑 Paste your Premium Key here:", type="password")

# Check if user is PRO
is_pro = (user_key == CORRECT_KEY)

if is_pro:
    st.sidebar.success("👑 PRO Status: Active (Unlimited Access)")
else:
    st.sidebar.info(f"⚪ Standard Status: Active ({3 - st.session_state.free_chat_count} Free AI Questions Left)")

# 4. Main App Interface
st.title("🧮 Afe's Homework Titan")
st.write("An online math homework helper equipped with a practice question mini calculator and math chat bot.")
st.write("---")

# --- FEATURE 1: AI MATH CHAT BOT ---
st.subheader("🤖 Titan AI Math Chat Bot")

# Display past chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Determine if they can chat
can_chat = is_pro or (st.session_state.free_chat_count < 3)

if can_chat:
    if user_prompt := st.chat_input("Type your math problem here (e.g., Solve 3x + 7 = 22)"):
        with st.chat_message("user"):
            st.write(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        # Count the question if they are a standard user
        if not is_pro:
            st.session_state.free_chat_count += 1

        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            system_instruction = "You are Afe's Homework Titan PRO. You are a brilliant, friendly math tutor for students. Break down equations step-by-step cleanly with final answers clearly shown."
            
            # 🔥 FIX: Changed model to gemini-3.6-flash
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=user_prompt,
                config={"system_instruction": system_instruction}
            )
            ai_response = response.text
        except Exception as e:
            ai_response = f"❌ Error connecting to AI: {str(e)}"

        with st.chat_message("assistant"):
            st.write(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Rerun to update the sidebar count instantly
        st.rerun()
else:
    st.error("⚠️ Free AI Questions Limit Reached!")
    st.write("You have used your 3 free questions. Please purchase a **PRO Premium Access Key** from the sidebar link to unlock unlimited AI step-by-step solutions!")

st.write("---")

# --- FEATURE 2: MINI CALCULATOR (Always Free for Standard Users!) ---
st.subheader("🧮 Titan Mini Calculator")
st.write("Perform standard calculations instantly.")

col1, col2 = st.columns(2)
with col1:
    num1 = st.number_input("Enter first number:", value=0.0, key="calc_num1")
with col2:
    num2 = st.number_input("Enter second number:", value=0.0, key="calc_num2")
    
operation = st.selectbox("Choose operation:", ["➕ Add", "➖ Subtract", "✖️ Multiply", "➕ Divide"], key="calc_op")

if st.button("Calculate Now"):
    if operation == "➕ Add":
        st.metric("Result", num1 + num2)
    elif operation == "➖ Subtract":
        st.metric("Result", num1 - num2)
    elif operation == "✖️ Multiply":
        st.metric("Result", num1 * num2)
    elif operation == "➕ Divide":
        if num2 != 0:
            st.metric("Result", num1 / num2)
        else:
            st.error("Cannot divide by zero!")
