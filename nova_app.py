import streamlit as st
import pandas as pd
import io
import speech_recognition as sr
from mic_recorder_streamlit import mic_recorder
from openai import OpenAI
from difflib import SequenceMatcher

# Initialize OpenAI client
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

# --- HEADER ---
st.title("🤖 Nova - Smart FAQ Assistant")
st.markdown("**Type your question or use the microphone 🎤**")

# --- MICROPHONE ---
audio_bytes = mic_recorder(
    start_prompt="🎤 Click to Record", 
    stop_prompt="⏹️ Stop", 
    key="mic"
)

user_input = ""

if audio_bytes:
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(io.BytesIO(audio_bytes["bytes"])) as source:
            audio = recognizer.record(source)
        user_input = recognizer.recognize_google(audio)
        st.success(f"🗣️ You said: {user_input}")
    except Exception as e:
        st.error(f"❌ Failed to process audio input.\n\n{e}")

# --- TEXT INPUT ---
typed_input = st.text_input("💬 Or type your question:")
if typed_input:
    user_input = typed_input

# --- FAQ DB (placeholder example) ---
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
        "Nova uses OpenAI’s GPT API to generate accurate responses to queries.",
        "Currently, Nova requires an internet connection to use OpenAI APIs.",
        "You can deploy Nova using Streamlit Cloud or any cloud provider.",
        "Nova was built by Solace as part of a smart assistant project."
    ]
})

# --- Function to find closest question ---
def get_best_match(query):
    highest = 0
    best_answer = "❌ Sorry, I couldn't find a relevant answer."
    for i, row in faq_data.iterrows():
        similarity = SequenceMatcher(None, query.lower(), row["question"].lower()).ratio()
        if similarity > highest and similarity > 0.5:
            highest = similarity
            best_answer = row["answer"]
    return best_answer

# --- PROCESS INPUT ---
if user_input:
    st.session_state.chat_history.append(("🧑 You", user_input))
    answer = get_best_match(user_input)
    st.session_state.chat_history.append(("🤖 Nova", answer))

# --- DISPLAY CHAT ---
st.divider()
for sender, msg in st.session_state.chat_history:
    with st.chat_message(sender):
        st.write(msg)
