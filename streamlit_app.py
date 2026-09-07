import streamlit as st
from google import genai

# 1. Page Configuration (Sets the title and emoji icon)
st.set_page_config(page_title="Afe's Homework Titan PRO", page_icon="🧮", layout="centered")

# 2. 🔑 SAFE KEYS: This pulls securely from your Streamlit Advanced Settings vault
# (Make sure to set these up in your Streamlit Cloud Secrets dashboard!)
CORRECT_KEY = st.secrets["DOWNLOAD_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# 3. Sidebar Configuration (The Store Front with your real Selar link)
st.sidebar.title("👑 Unlock Titan PRO")
st.sidebar.write("Get instant access to the ultimate math homework helper!")

# 🌟 YOUR EXACT SELAR LINK LISTED FOR 2,500 NGN
st.sidebar.markdown("[👉 CLICK HERE TO BUY YOUR KEY (2,500 NGN) 👈](https://selar.com)")
st.sidebar.write("---")

# User types the key they bought and downloaded from your Premium_key.txt file here
user_key = st.sidebar.text_input("🔑 Paste your Premium Key here:", type="password")

# 4. Main App Interface
st.title("🧮 Afe's Homework Titan PRO")
st.write("An online math homework helper equipped with a practice question mini calculator and math chat bot.")
st.write("---")

# 5. Check if the Premium Key entered by the user matches your secret key
if user_key == CORRECT_KEY:
    st.success("🎉 Access Granted! Welcome to PRO Mode.")
    
    # --- FEATURE 1: REAL AI MATH CHAT BOT ---
    st.subheader("🤖 Titan AI Math Chat Bot")
    st.write("Ask any math problem. The AI will explain it step-by-step!")

    # Initialize chat history so the AI remembers previous messages in the conversation
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am the Titan Math AI. Paste your math problem here!"}
        ]

    # Display past chat messages on the screen
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat Input Box at the bottom of the screen
    if user_prompt := st.chat_input("Type your math problem here (e.g., Solve 3x + 7 = 22)"):
        # Display user message instantly
        with st.chat_message("user"):
            st.write(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        try:
            # Set up the real AI client using your Gemini key
            client = genai.Client(api_key=GEMINI_API_KEY)
            
            # Give the AI strict instructions to act like a friendly math teacher
            system_instruction = "You are Afe's Homework Titan PRO. You are a brilliant, friendly math tutor for students. Break down equations step-by-step cleanly."
            
            # Request response from Gemini model
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_prompt,
                config={"system_instruction": system_instruction}
            )
            ai_response = response.text
        except Exception as e:
            ai_response = f"❌ Error connecting to AI: {str(e)}"

        # Display AI response on the screen
        with st.chat_message("assistant"):
            st.write(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

    st.write("---")

    # --- FEATURE 2: MINI CALCULATOR ---
    st.subheader("🧮 Titan Mini Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        num1 = st.number_input("Enter first number:", value=0.0)
    with col2:
        num2 = st.number_input("Enter second number:", value=0.0)
        
    operation = st.selectbox("Choose operation:", ["➕ Add", "➖ Subtract", "✖️ Multiply", "➕ Divide"])
    
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

else:
    # 6. What Unpaid/Locked Users See
    st.warning("⚠️ **PRO Features Locked**")
    st.write("Please purchase a Premium Access Key from the link in the sidebar to unlock the Titan Math Brain.")
    
    st.info("💡 **Free Tester:** Try solving standard addition below to test the Titan speed!")
    free_test = st.text_input("What is 5 + 5?")
    if free_test == "10":
        st.success("Correct! Buy the PRO Key to unlock hard algebra, word problems, and graphing help!")
