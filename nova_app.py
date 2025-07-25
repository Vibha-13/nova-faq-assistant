import streamlit as st
from streamlit_audio import st_audio
import openai
import os
from dotenv import load_dotenv
import tempfile

# Load your API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- CONFIGURE PAGE ---
st.set_page_config(page_title="Nova FAQ Assistant", layout="centered")

# --- SIDEBAR ---
st.sidebar.image("nova_bot.png", use_column_width=True)
st.sidebar.title("Nova - FAQ Chatbot")
st.sidebar.markdown("Ask anything related to our services ✨")
st.sidebar.markdown("Voice or Text input supported 🎤⌨️")

# --- MAIN INTERFACE ---
st.title("🎙️ Nova - Ask Your Question")

st.markdown("### Option 1: Record your voice below 👇")
audio_bytes = st_audio(start_prompt="Click to record", stop_prompt="Click again to stop")

st.markdown("### Option 2: Or type your question ⌨️")
text_input = st.text_input("Type your question here:")

query = None

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        tmpfile.write(audio_bytes)
        tmpfile_path = tmpfile.name

    with st.spinner("Transcribing your question..."):
        with open(tmpfile_path, "rb") as f:
            transcript = openai.Audio.transcribe("whisper-1", f)
            query = transcript["text"]
        st.markdown("#### 📝 Transcription:")
        st.write(query)

elif text_input:
    query = text_input

# --- PROCESS QUERY ---
if query:
    with st.spinner("Nova is thinking... 💭"):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}]
        )
        answer = response["choices"][0]["message"]["content"]

    st.markdown("### 🤖 Nova Says:")
    st.write(answer)
