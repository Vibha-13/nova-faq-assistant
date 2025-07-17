import streamlit as st
import openai
import speech_recognition as sr
from pydub import AudioSegment
import os
import tempfile
import time
import pyttsx3
import random

# Configure Page
st.set_page_config(page_title="Nova AI Assistant", page_icon="🧠", layout="centered")

# Title and Subtitle
st.markdown("<h1 style='text-align: center;'>🎙️ Nova - Your Voice AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload your voice. Nova listens, replies, speaks, and motivates you ✨</p>", unsafe_allow_html=True)

# Load OpenAI API Key
openai.api_key = st.secrets.get("OPENAI_API_KEY", "your-api-key-here")  # Replace if not using secrets

# Sidebar - Nova Tips
st.sidebar.markdown("### 💡 Nova Tips")
st.sidebar.info("Use clear voice when recording.\n\nSupports `.wav`, `.mp3`, `.m4a` files.\n\nMax 1 min voice for best results.")
st.sidebar.markdown("---")

# Motivational Quotes Carousel
quotes = [
    "🌟 Keep going, you're doing amazing!",
    "🔥 Success is built on persistence, not perfection.",
    "🌈 Storms make trees take deeper roots.",
    "💫 One small voice can spark big change.",
    "🚀 You were born to make magic!"
]
if st.sidebar.button("✨ Inspire Me!"):
    st.sidebar.success(random.choice(quotes))

# File uploader
uploaded_audio = st.file_uploader("🎧 Upload your voice file", type=["wav", "mp3", "m4a"])

# Store conversation history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Text-to-Speech setup
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak_text(text):
    """Speak the text using pyttsx3 (works locally)"""
    engine.say(text)
    engine.runAndWait()

# Handle upload
if uploaded_audio:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio_file:
        audio_format = uploaded_audio.type.split("/")[1]
        if audio_format == "mp3":
            sound = AudioSegment.from_mp3(uploaded_audio)
        elif audio_format == "m4a":
            sound = AudioSegment.from_file(uploaded_audio, format="m4a")
        else:
            sound = AudioSegment.from_file(uploaded_audio)

        sound.export(tmp_audio_file.name, format="wav")

        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_audio_file.name) as source:
            st.info("🔍 Transcribing your voice...")
            audio_data = recognizer.record(source)

        try:
            user_input = recognizer.recognize_google(audio_data)
            st.success(f"🗣️ You said: **{user_input}**")

            with st.spinner("🤖 Nova is thinking..."):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are Nova, a friendly and empathetic voice AI assistant."},
                        {"role": "user", "content": user_input}
                    ]
                )
                ai_reply = response['choices'][0]['message']['content']

                # Emoji response animation
                st.markdown("### 🤖 Nova replies:")
                for word in ai_reply.split():
                    st.markdown(f"{word} ", unsafe_allow_html=True)
                    time.sleep(0.05)

                # Add to session history
                st.session_state.chat_history.append((user_input, ai_reply))

                # Nova speaks (if running locally)
                try:
                    speak_text(ai_reply)
                except Exception:
                    st.warning("🔇 Voice reply not supported on cloud. Run locally to hear Nova.")

        except sr.UnknownValueError:
            st.error("😕 Couldn't understand your audio. Try speaking more clearly.")
        except sr.RequestError:
            st.error("🚫 Speech recognition service unavailable.")

    os.remove(tmp_audio_file.name)

# Chat History Display
if st.session_state.chat_history:
    st.markdown("## 💬 Chat History")
    for i, (q, a) in enumerate(st.session_state.chat_history[::-1], 1):
        st.markdown(f"**🧍 You:** {q}")
        st.markdown(f"**🤖 Nova:** {a}")
        st.markdown("---")

# Download chat history
if st.session_state.chat_history:
    if st.button("📥 Download Conversation"):
        chat_log = "\n\n".join([f"You: {q}\nNova: {a}" for q, a in st.session_state.chat_history])
        st.download_button("📁 Download .txt", data=chat_log, file_name="nova_conversation.txt")

