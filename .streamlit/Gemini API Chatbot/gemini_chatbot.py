# ──────────────────────────────────────────────────────────────
# 1. CONFIGURATION AND SETUP
# ──────────────────────────────────────────────────────────────
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 GEMINI_API_KEY not found. Please add it to your .env file.")
    st.stop()

# Configure the Gemini API
genai.configure(api_key=api_key)

# Define the model explicitly
MODEL_NAME = "gemini-3-flash-preview"  

# ──────────────────────────────────────────────────────────────
# 2. STREAMLIT UI
# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Gemini API Chatbot", page_icon=":robot_face:")
st.title("✨ Gemini Query Assistant")
st.caption("Powered by Google's Gemini Flash model")

# Initialize chat history & Gemini chat session
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.gemini_chat = genai.GenerativeModel(MODEL_NAME).start_chat(history=[])

# Display existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ──────────────────────────────────────────────────────────────
# 3. HANDLE USER INPUT & GENERATE RESPONSE
# ──────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask me anything..........."):
    # 1️⃣ Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2️⃣ Generate & show assistant response
    with st.chat_message("assistant"):
        with st.spinner("Gemini is thinking..."):
            try:
                response = st.session_state.gemini_chat.send_message(prompt)
                
                if not response.text:
                    st.warning("⚠️ The model returned an empty response. It may have filtered the query.")
                else:
                    st.markdown(response.text)
                    # ✅ Fixed typo: "assistance" -> "assistant"
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})