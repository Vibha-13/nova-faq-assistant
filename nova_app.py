import streamlit as st
import pandas as pd
from openai import OpenAI
import base64
import io
import tempfile
from pydub import AudioSegment
import speech_recognition as sr
from streamlit_js_eval import streamlit_js_eval
from difflib import SequenceMatcher

client = OpenAI()

st.set_page_config(page_title="Nova - Smart FAQ Assistant", layout="wide")

# --- SIDEBAR ---
st.sidebar.title("🤖 Nova - Smart FAQ Assistant")
st.sidebar.markdown("Ask me anything about your project, usage, or deployment!")
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat_history = []

# --- SESSION ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🤖 Nova - Smart FAQ Assistant")
st.markdown("**Type your question or use the microphone 🎤**")

# --- JS RECORDING ---
audio_data = streamlit_js_eval(js_expressions="record_audio", key="audio")

user_input = ""

if audio_data:
    try:
        audio_bytes = base64.b64decode(audio_data.split(",")[1])
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        audio = AudioSegment.from_file(tmp_path)
        audio.export(tmp_path, format="wav")

        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_path) as source:
            audio = recognizer.record(source)
        user_input = recognizer.recognize_google(audio)
        st.success(f"🗣️ You said: {user_input}")
    except Exception as e:
        st.error(f"❌ Voice input failed: {e}")

# --- TEXT INPUT ---
typed_input = st.text_input("💬 Or type your question:")
if typed_input:
    user_input = typed_input

# --- FAQ DB (placeholder) ---
faq_data = pd.DataFrame({
    "question": [
        "What is Nova?",
        "How does Nova use AI?",
        "Can Nova work offline?",
        "How to deploy Nova?",
        "Who built Nova?"
    ],
    "answer": [
        "Nova is a Smart FAQ Assistant built using Streamlit and OpenAI.",
        "Nova uses OpenAI’s GPT API to generate accurate responses.",
        "Currently, Nova requires internet to connect to OpenAI APIs.",
        "You can deploy Nova on Streamlit Cloud or other platforms.",
        "Nova was built by Solace as a personal project."
    ]
})

def get_best_match(query):
    highest = 0
    best_answer = "❌ Sorry, I couldn't find a relevant answer."
    for i, row in faq_data.iterrows():
        similarity = SequenceMatcher(None, query.lower(), row["question"].lower()).ratio()
        if similarity > highest and similarity > 0.5:
            highest = similarity
            best_answer = row["answer"]
    return best_answer

if user_input:
    st.session_state.chat_history.append(("🧑 You", user_input))
    answer = get_best_match(user_input)
    st.session_state.chat_history.append(("🤖 Nova", answer))

st.divider()
for sender, msg in st.session_state.chat_history:
    with st.chat_message(sender):
        st.write(msg)
