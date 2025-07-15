import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from difflib import SequenceMatcher
import tempfile
import base64
import speech_recognition as sr
from pydub import AudioSegment
import io
from streamlit_mic_recorder import mic_recorder

# 🎯 API Setup (Together API)
api_key = st.secrets["together"]["api_key"]
client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# 📁 Load FAQ file
FAQ_FILE = "faqs.csv"
if not os.path.exists(FAQ_FILE):
    st.error("🚨 FAQ file not found! Please ensure 'faqs.csv' is in the app folder.")
    st.stop()

df = pd.read_csv(FAQ_FILE)
faq_qa = list(zip(df["Question"].astype(str), df["Answer"].astype(str)))

# 🌐 App config
st.set_page_config(page_title="Nova - Smart FAQ Assistant", page_icon="🤖")

# 📸 Sidebar
with st.sidebar:
    try:
        st.image("nova_bot.png", caption="Nova, your smart assistant 🤖", use_container_width=True)
    except:
        st.info("🖼️ Nova image not found (optional).")
    st.markdown("### Built with 💙 by Solace & Nyx")
    st.markdown("---")
    st.markdown("🧹 Want to clear the chat?")
    if st.button("Clear Chat"):
        st.session_state.chat_history = []

# 🧠 Memory init
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🧠 Main UI
st.title("🤖 Nova - Smart FAQ Assistant")
st.markdown("Type your question or use the microphone 🎤")

# 🎤 Voice Input
audio_bytes = mic_recorder(start_prompt="🎙️ Record", stop_prompt="🛑 Stop", just_once=True, key="mic")

# 📝 Text Input
user_question = st.text_input("💬 Or type your question:")

# 🎤 Voice Recognition
if audio_bytes and "bytes" in audio_bytes:
    try:
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes["bytes"]))
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav_file:
            audio.export(tmp_wav_file.name, format="wav")
            temp_audio_path = tmp_wav_file.name

        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = recognizer.record(source)
            try:
                user_question = recognizer.recognize_google(audio_data)
                st.success(f"🗣️ You asked: {user_question}")
            except sr.UnknownValueError:
                st.warning("😕 Sorry, couldn't understand your voice.")
            except sr.RequestError:
                st.error("❌ Could not connect to Google API.")
    except Exception as e:
        st.error("❌ Failed to process audio input.")
        st.exception(e)

# 🔍 Process the question
if user_question:
    def similarity(a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    best_match = None
    best_score = 0.0
    for q, a in faq_qa:
        score = similarity(user_question, q)
        if score > best_score:
            best_score = score
            best_match = (q, a)

    if best_score > 0.6:
        answer = best_match[1]
        st.success(f"✅ Found a relevant FAQ (Similarity: {best_score:.2f})")
        st.markdown(f"**Q:** {best_match[0]}")
        st.markdown(f"**🧠 Nova says:** {answer}")
    else:
        st.warning("🤔 No close FAQ found. Asking GPT...")
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are Nova, a helpful and friendly AI assistant."},
                    {"role": "user", "content": user_question}
                ]
            )
            answer = response.choices[0].message.content.strip()
            st.markdown("**🤖 Nova says:**")
            st.info(answer)
        except Exception as e:
            st.error("❌ GPT failed to respond.")
            st.exception(e)

    # 💬 Add to chat history
    st.session_state.chat_history.append(("You", user_question))
    st.session_state.chat_history.append(("Nova", answer))

# 💬 Display chat history
if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("🧠 Chat History")
    for speaker, message in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"**🧍 You:** {message}")
        else:
            st.markdown(f"**🤖 Nova:** {message}")
