import streamlit as st
import openai
import base64
from pathlib import Path

# Set page config
st.set_page_config(page_title="Nova - FAQ Assistant", page_icon="🤖", layout="centered")

# Optional audio recorder support
try:
    from streamlit_audiorecorder import audiorecorder
except ModuleNotFoundError:
    audiorecorder = None
    st.warning("⚠️ Audio recording not available. This feature is optional.")

# Set up your OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]


# Sidebar with branding
st.sidebar.image("nova_bot.png", width=100)
st.sidebar.title("Nova - Audio FAQ Assistant")
st.sidebar.markdown("Ask me your college FAQs 👩🏻‍💻🎓")

# App title
st.title("🎙️ Talk to Nova")
st.markdown("Record your question, and I'll do my best to help!")

# Record audio if available
audio_bytes = None
if audiorecorder:
    audio_bytes = audiorecorder("🎤 Record", "⏹️ Stop")
else:
    st.info("You can still use the chat if mic input is disabled.")

# Simulate transcribing (placeholder for real speech-to-text)
def dummy_transcribe(audio_bytes):
    # In real app, replace with OpenAI Whisper or other STT model
    return "What is the eligibility for campus placement?"

# Simulate AI answer (replace with actual API call or fine-tuned model)
def get_answer(query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or gpt-4 if available
        messages=[
            {"role": "system", "content": "You are Nova, a helpful assistant for college FAQs."},
            {"role": "user", "content": query}
        ]
    )
    return response["choices"][0]["message"]["content"]

# Process audio
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    st.write("Transcribing...")
    query = dummy_transcribe(audio_bytes)
    st.write(f"**You asked:** {query}")
    with st.spinner("Nova is thinking..."):
        answer = get_answer(query)
        st.success(answer)
else:
    st.markdown("⬆️ Press the button to start recording your question.")

