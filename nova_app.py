import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from difflib import SequenceMatcher
from streamlit_webrtc import webrtc_streamer
import tempfile
import speech_recognition as sr
import av
import numpy as np

# 🌐 Together AI setup
api_key = st.secrets["together"]["api_key"]
client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# 📁 Load FAQ file
FAQ_FILE = "faqs.csv"
if not os.path.exists(FAQ_FILE):
    st.error("🚨 FAQ file not found! Please ensure 'faqs.csv' is in the app folder.")
    st.stop()

df = pd.read_csv(FAQ_FILE)
faq_qa = list(zip(df["Question"].astype(str), df["Answer"].astype(str)))

# 🎨 Page config
st.set_page_config(page_title="Nova - Smart FAQ Assistant", page_icon="🤖")

# 📸 Sidebar
with st.sidebar:
    st.image("nova_bot.png", caption="Nova, your smart assistant 🤖", use_container_width=True)
    st.markdown("### Built by **Solace** & **Nyx** ✨")
    st.markdown("---")
    if st.button("🧹 Clear Chat History"):
        st.session_state.messages = []
        st.experimental_rerun()

# 🔁 Session state setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🧠 Similarity check
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# 🧾 Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🎙️ Voice-to-text capture
st.markdown("**🎤 Speak your question or type below**")
webrtc_ctx = webrtc_streamer(key="speech", audio_receiver_size=256, async_processing=False)

# 🧠 Convert audio to text
def transcribe_audio(audio_bytes):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        tmpfile.write(audio_bytes)
        tmpfile_path = tmpfile.name
    with sr.AudioFile(tmpfile_path) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return None

user_question = st.chat_input("💬 Type your question here:")

# Check for voice input
if webrtc_ctx and webrtc_ctx.audio_receiver:
    audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=2)
    if audio_frames:
        audio = b"".join([f.to_ndarray().tobytes() for f in audio_frames if isinstance(f, av.AudioFrame)])
        voice_text = transcribe_audio(audio)
        if voice_text:
            user_question = voice_text
            st.success(f"🗣️ You said: {user_question}")
        else:
            st.warning("😓 Couldn’t understand audio. Try again.")

# 🚀 Handle the question
if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    best_match = None
    best_score = 0.0
    for q, a in faq_qa:
        score = similarity(user_question, q)
        if score > best_score:
            best_score = score
            best_match = (q, a)

    if best_score > 0.6:
        answer = best_match[1]
        st.success(f"✅ Found a relevant FAQ (Similarity: {best_score:.2f})")
    else:
        with st.spinner("🤔 Asking Nova..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are Nova, a helpful AI FAQ assistant who answers clearly and encouragingly."},
                        {"role": "user", "content": user_question}
                    ]
                )
                answer = response.choices[0].message.content.strip()
            except Exception as e:
                st.error("❌ GPT failed to respond.")
                st.exception(e)
                answer = "Sorry, I couldn't fetch an answer."

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
