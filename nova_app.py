import streamlit as st
import openai
import os
from dotenv import load_dotenv
from streamlit_audiorecorder import audiorecorder
from pydub import AudioSegment
import base64
import tempfile

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# -------------------- Theme & Sidebar --------------------
st.set_page_config(page_title="Nova Voice Assistant 🤖", page_icon="🧠", layout="centered")

with st.sidebar:
    st.image("nova_bot.png", use_column_width=True)
    st.title("Nova - FAQ Assistant 🤖")
    st.markdown("Ask your college-related questions using **voice or text**!")
    st.markdown("---")
    st.write("🎙️ Record your question or 🧠 type below.")

# -------------------- Emoji Header --------------------
st.markdown("## 🎓 Nova: Your College FAQ Voice Assistant")

# -------------------- Audio Recording --------------------
audio = audiorecorder("Click to record 🎙️", "Recording... 🔴")

user_question = ""

if len(audio) > 0:
    st.audio(audio.export().read(), format="audio/wav")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        audio.export(tmpfile.name, format="wav")
        tmpfile_path = tmpfile.name

    sound = AudioSegment.from_wav(tmpfile_path)
    sound.export("user_question.mp3", format="mp3")

    with open("user_question.mp3", "rb") as f:
        audio_data = f.read()

    st.info("🧠 Converting your voice to text...")

    try:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=("user_question.mp3", audio_data)
        )
        user_question = transcript.text
        st.success(f"🗣️ You asked: **{user_question}**")
    except Exception as e:
        st.error("❌ Error transcribing audio: " + str(e))

# -------------------- Text Input Fallback --------------------
st.markdown("### Or type your question below:")
typed_input = st.text_input("💬 Your question here:")

if typed_input:
    user_question = typed_input

# -------------------- Process with GPT --------------------
if user_question:
    with st.spinner("Nova is thinking... 🧠"):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Nova, a helpful college assistant. Keep responses clear and friendly."},
                    {"role": "user", "content": user_question}
                ]
            )
            reply = response.choices[0].message.content
            st.markdown(f"### 📢 Nova says:\n{reply}")
        except Exception as e:
            st.error("❌ Error from OpenAI: " + str(e))
