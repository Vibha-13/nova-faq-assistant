import streamlit as st
import openai
import os
import speech_recognition as sr
from io import BytesIO
from PIL import Image
import base64

# Load API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Page settings
st.set_page_config(page_title="Nova - FAQ Assistant 💬", page_icon="🤖", layout="wide")

# Sidebar with Nova image
with st.sidebar:
    st.image("nova_bot.png", width=150)
    st.title("✨ Nova Assistant")
    st.markdown("Your friendly FAQ chatbot 💡")
    st.markdown("Ask me anything from your syllabus or training notes!")

# Title
st.markdown("<h2 style='text-align:center;'>👩‍💻 Nova - Your FAQ Assistant</h2>", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.text_input("🗨️ Ask Nova a question...", placeholder="Type your question here...")

# Speech recognition (optional)
if st.button("🎤 Use Voice"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now.")
        audio = recognizer.listen(source, timeout=5)
    try:
        user_input = recognizer.recognize_google(audio)
        st.success(f"You said: {user_input}")
    except sr.UnknownValueError:
        st.error("Couldn't understand audio.")
    except sr.RequestError:
        st.error("Speech recognition service is unavailable.")

# Handle user query
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append(("🧑‍💻 You", user_input))
    
    try:
        # Call OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4 if you have access
            messages=[
                {"role": "system", "content": "You are Nova, a helpful educational chatbot."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        st.session_state.chat_history.append(("🤖 Nova", reply))

    except Exception as e:
        st.session_state.chat_history.append(("🤖 Nova", "⚠️ Nova couldn't reach OpenAI servers. Try again later."))

# Display chat history
st.markdown("### 📜 Chat History")
for sender, message in st.session_state.chat_history[::-1]:
    with st.chat_message(sender):
        st.markdown(message)
