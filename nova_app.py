import streamlit as st
from openai import OpenAI
import os
import io
from mic_recorder_streamlit import mic_recorder
from pydub import AudioSegment
import speech_recognition as sr
from difflib import SequenceMatcher

# Set OpenAI API Key from secrets
client = OpenAI(api_key=st.secrets["api_key"])

# Page config
st.set_page_config(page_title="Nova - Smart FAQ Assistant", page_icon="🤖", layout="centered")

# Sidebar with app title and image
with st.sidebar:
    st.image("https://i.imgur.com/Z6G7c9k.png", width=120)
    st.markdown("## 🤖 Nova - Smart FAQ Assistant")
    st.markdown("Ask your doubts via text or mic 🎤")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Title
st.markdown("### 🧠 Type your question or use the microphone 🎤")

# Mic recorder
audio_bytes = mic_recorder(start_prompt="🎙 Click to Speak", stop_prompt="⏹ Stop", just_once=True, use_container_width=True)

# Text input fallback
user_question = st.text_input("💬 Or type your question:")

# Handle audio input
if audio_bytes and not user_question:
    try:
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes["bytes"]))
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            audio.export(f.name, format="wav")
            temp_audio_path = f.name

        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_audio_path) as source:
            recorded_audio = recognizer.record(source)
        user_question = recognizer.recognize_google(recorded_audio)

        os.remove(temp_audio_path)  # Clean up

    except Exception as e:
        st.error(f"❌ Failed to process audio input.\n\n{e}")

# If there's a question, call OpenAI
if user_question:
    with st.spinner("🤔 Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Nova, a smart FAQ assistant. Keep answers helpful and short."},
                    {"role": "user", "content": user_question}
                ]
            )
            answer = response.choices[0].message.content
            # Save to session state
            st.session_state.chat_history.append(("🧑‍💻", user_question))
            st.session_state.chat_history.append(("🤖", answer))
        except Exception as e:
            st.error(f"❌ OpenAI error: {e}")

# Display chat history
for sender, msg in st.session_state.chat_history:
    with st.chat_message(sender):
        st.markdown(msg)
