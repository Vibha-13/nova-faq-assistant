import streamlit as st
from streamlit_audiorecorder import audiorecorder
from pydub import AudioSegment
import openai
import io
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit page setup
st.set_page_config(page_title="Nova - Audio FAQ Assistant", page_icon="🎧")
st.title("Nova - Audio FAQ Assistant")
st.subheader("Ask me your college FAQs 👩🏻‍💻🎓")

st.markdown(
    "⚠️ **Audio recording not available**. This feature is optional.\n\n"
    "🎙️ **Talk to Nova**  \n"
    "Record your question, and I'll do my best to help!\n\n"
    "_You can still use the chat if mic input is disabled._\n\n"
    "⬆️ Press the button to start recording your question."
)

# Function to ask OpenAI
def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can change to gpt-4 if available
            messages=[
                {"role": "system", "content": "You are Nova, a friendly assistant for college-related FAQs."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"❌ Error: {e}"

# 1. Try Audio Input
audio_data = audiorecorder("🎙️ Record", "⏹️ Stop")

if audio_data:
    st.audio(audio_data, format="audio/wav")

    with st.spinner("Transcribing your question..."):
        audio = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")
        buffered = io.BytesIO()
        audio.export(buffered, format="mp3")
        buffered.seek(0)

        try:
            transcript = openai.Audio.transcribe("whisper-1", buffered)
            question = transcript["text"]
            st.success(f"📝 You said: {question}")

            with st.spinner("Nova is thinking..."):
                response = ask_openai(question)
                st.chat_message("assistant").markdown(response)

        except Exception as e:
            st.error(f"❌ Audio transcription failed: {e}")

# 2. Fallback: Text Input if Mic Not Available
else:
    st.info("🎤 Mic input not available or not used. You can type your question below.")
    text_question = st.chat_input("Type your question here 👇")

    if text_question:
        with st.spinner("Nova is thinking..."):
            response = ask_openai(text_question)
            st.chat_message("assistant").markdown(response)
