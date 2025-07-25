import streamlit as st
import openai
import os
from dotenv import load_dotenv
from audiorecorder import audiorecorder
from pydub import AudioSegment
import base64
import tempfile

# Load the .env file (API keys)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set page config
st.set_page_config(
    page_title="Nova Audio FAQ Assistant 🤖🎧",
    layout="centered",
    page_icon="🎙️",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.image("nova_bot.png", width=200)
    st.markdown("## 👋 Welcome to Nova!")
    st.markdown("Ask your college FAQs via voice.")
    st.markdown("#### 💡 Tip: Speak clearly into your mic.")
    st.markdown("---")
    st.markdown("Made with ❤️ by Team Nova")

st.title("🎧 Ask Nova: Your FAQ Audio Assistant")

# Audio recording
audio = audiorecorder("🎤 Record", "🔴 Stop")

if len(audio) > 0:
    with st.spinner("Transcribing your question..."):
        # Save to temp WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            audio.export(f.name, format="wav")
            temp_path = f.name

        # Send to OpenAI Whisper
        audio_file = open(temp_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

        st.success("✅ Transcription Complete!")
        st.markdown(f"**📝 You asked:** `{transcript['text']}`")

        # Send to GPT
        with st.spinner("Fetching Nova's answer..."):
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You're Nova, a helpful assistant answering college FAQ questions."},
                    {"role": "user", "content": transcript["text"]}
                ]
            )
            answer = completion.choices[0].message["content"]
            st.markdown("### 🧠 Nova says:")
            st.success(answer)
