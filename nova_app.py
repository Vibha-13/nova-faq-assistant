import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
import tempfile
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# --- SETUP ---
st.set_page_config(page_title="Nova - FAQ Assistant", layout="centered")

# --- SIDEBAR ---
st.sidebar.image("nova_bot.png", use_column_width=True)
st.sidebar.title("Nova - FAQ Chatbot")
st.sidebar.markdown("Ask anything related to our services ✨")
st.sidebar.markdown("Voice or Text input supported 🎤⌨️")

# --- MAIN TITLE ---
st.title("🎙️ Nova - Voice FAQ Assistant")

# --- AUDIO RECORDER ---
audio_bytes = audio_recorder(
    text="Click to record your question 🎤",
    recording_color="#f65f5f",
    neutral_color="#6aa36f",
    icon_size="3x"
)

# --- TEXT FALLBACK ---
st.markdown("### Or just type your question below ⌨️")
text_input = st.text_input("Enter your question here:")

# --- HANDLE AUDIO OR TEXT INPUT ---
query = None

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    
    with st.spinner("Transcribing your voice..."):
        # Save the audio to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            tmpfile.write(audio_bytes)
            tmpfile_path = tmpfile.name

        # Transcribe using Whisper
        with open(tmpfile_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)

        query = transcript["text"]
        st.markdown("#### 📝 Transcription:")
        st.write(query)

elif text_input:
    query = text_input

# --- CALL OPENAI API IF QUERY EXISTS ---
if query:
    with st.spinner("Nova is thinking... 💭"):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}]
        )
        answer = response["choices"][0]["message"]["content"]
        
    st.markdown("### 🤖 Nova says:")
    st.write(answer)
