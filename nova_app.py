import streamlit as st
import os
import io
import base64
import speech_recognition as sr
from pydub import AudioSegment
from openai import OpenAI
from difflib import SequenceMatcher
from datetime import datetime

# ⬛ OpenAI client setup
client = OpenAI(api_key=st.secrets["api_key"])

# ⬛ Page config and styling
st.set_page_config(page_title="Nova - Smart FAQ Assistant", page_icon="🤖", layout="wide")
st.markdown("<h1 style='text-align: center;'>🤖 Nova - Smart FAQ Assistant</h1>", unsafe_allow_html=True)
st.markdown("---")

# ⬛ Sidebar with clear button and about info
with st.sidebar:
    st.image("https://i.ibb.co/gFt1FWH/nova-bot.png", use_column_width=True)
    st.markdown("## 💬 Chat History")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for i, (q, a) in enumerate(reversed(st.session_state.chat_history[-5:])):
        st.markdown(f"**Q{i+1}:** {q}\n> {a}")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
    st.markdown("---")
    st.markdown("Made with ❤️ by Solace")

# ⬛ Helper function to check similarity between question and preset FAQ list
faq_answers = {
    "what is nova": "Nova is your AI-powered FAQ assistant developed using Streamlit and OpenAI.",
    "how does nova work": "Nova listens to your question (text or voice), understands it, and gives helpful answers using AI.",
    "who created nova": "Nova was created by Solace 💡",
    "can nova take voice input": "Yes! Nova can take voice input via your mic 🎤 and convert it to text before answering."
}

def find_faq_answer(user_question):
    user_question = user_question.lower()
    best_match = None
    highest_ratio = 0.6
    for faq in faq_answers:
        ratio = SequenceMatcher(None, user_question, faq).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = faq
    return faq_answers.get(best_match, None)

# ⬛ Voice recorder
st.markdown("### 🎤 Speak your question (or type below)")

# 📣 JS-based microphone recorder (no need for streamlit-webrtc)
audio_bytes = st.file_uploader("Upload your voice question (WAV/MP3)", type=["wav", "mp3"])

user_question = ""

if audio_bytes:
    try:
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes.read()))
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)
            user_question = recognizer.recognize_google(audio_data)
        st.success(f"🗣️ You said: {user_question}")

    except Exception as e:
        st.error("❌ Failed to process audio input.")
        st.error(str(e))

# ⬛ Or type the question
user_text_input = st.text_input("💬 Or type your question:", key="text_input")
if user_text_input:
    user_question = user_text_input

# ⬛ Handle user question
if user_question:
    with st.spinner("Thinking..."):
        faq_response = find_faq_answer(user_question)
        if faq_response:
            answer = faq_response
        else:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Nova, a helpful assistant who answers user FAQs in simple language."},
                    {"role": "user", "content": user_question}
                ]
            )
            answer = response.choices[0].message.content

    # Save to chat history and display
    st.session_state.chat_history.append((user_question, answer))
    st.markdown(f"### 🤖 Nova says:
{answer}")
