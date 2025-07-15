import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from difflib import SequenceMatcher
from streamlit_audio_recorder import audio_recorder
import base64
import tempfile
import speech_recognition as sr

# 🎯 Together AI Setup
api_key = st.secrets["together"]["api_key"]
client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# 🎨 Page Config
st.set_page_config(page_title="Nova - Smart FAQ Assistant", page_icon="🤖")

# 📸 Sidebar UI
with st.sidebar:
    if os.path.exists("nova_bot.png"):
        st.image("nova_bot.png", caption="Nova, your smart assistant 🤖", use_container_width=True)
    else:
        st.warning("⚠️ 'nova_bot.png' not found.")
    
    st.markdown("### Built by **Solace** & **Nyx** ✨")
    st.markdown("---")
    st.markdown("💬 Ask me by typing or speaking 🎤")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []

# 📁 Load FAQ
FAQ_FILE = "faqs.csv"

@st.cache_data
def load_faq():
    return pd.read_csv(FAQ_FILE)

if not os.path.exists(FAQ_FILE):
    st.error("🚨 'faqs.csv' not found. Add it and reload.")
    st.stop()

df = load_faq()
faq_qa = list(zip(df["Question"].astype(str), df["Answer"].astype(str)))

# 💬 Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Nova - Smart FAQ Assistant")
st.markdown("Ask by typing or use your voice 🎤")

# 🎤 Voice Recorder
audio_bytes = audio_recorder(pause_threshold=1.0, sample_rate=44100)
user_input = None

# ✨ Convert Audio to Text
if audio_bytes:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        tmpfile.write(audio_bytes)
        tmpfile_path = tmpfile.name

    recognizer = sr.Recognizer()
    with sr.AudioFile(tmpfile_path) as source:
        audio_data = recognizer.record(source)
        try:
            user_input = recognizer.recognize_google(audio_data)
            st.success(f"🗣️ You said: **{user_input}**")
        except sr.UnknownValueError:
            st.error("❌ Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"⚠️ Speech recognition error: {e}")

# ✏️ Text Input fallback
typed_input = st.chat_input("Ask your question...")
if typed_input:
    user_input = typed_input

# 🔍 Similarity function
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# 🔁 Process Input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Step 1: FAQ Match
    best_match = None
    best_score = 0.0
    for q, a in faq_qa:
        score = similarity(user_input, q)
        if score > best_score:
            best_score = score
            best_match = (q, a)

    if best_score > 0.6:
        reply = best_match[1]
    else:
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are Nova, a helpful and warm AI assistant trained on FAQ data."}
                ] + st.session_state.messages
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"⚠️ GPT failed: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})

# 💬 Display Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
