import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from difflib import SequenceMatcher
import tempfile
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer
import av
import numpy as np
from scipy.io.wavfile import write
import queue

# 📌 App Config
st.set_page_config(page_title="Nova - Smart FAQ Assistant", page_icon="🤖", layout="wide")

# 🌐 API Setup
api_key = st.secrets["together"]["api_key"]
client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# 📁 Load FAQs
FAQ_FILE = "faqs.csv"
if not os.path.exists(FAQ_FILE):
    st.error("🚨 FAQ file not found! Please ensure 'faqs.csv' is in the app folder.")
    st.stop()

df = pd.read_csv(FAQ_FILE)
faq_qa = list(zip(df["Question"].astype(str), df["Answer"].astype(str)))

# 💬 Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🎨 Sidebar
with st.sidebar:
    st.image("nova_bot.png", caption="Nova, your smart assistant 🤖", use_container_width=True)
    st.markdown("### Built by **Solace** & **Nyx** ✨")
    st.markdown("---")
    st.markdown("💡 Ask your question or use the mic to speak.")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.experimental_rerun()

# 🧠 Similarity Logic
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# 🗣️ Voice Input Section
st.markdown("### 🎤 Speak your question (or type below)")
text_input = ""

with st.expander("🎧 Click to record audio"):
    webrtc_ctx = webrtc_streamer(
        key="speech",
        mode="sendonly",
        in_audio=True,
        audio_receiver_size=256,
        sendback_audio=False,
        media_stream_constraints={"audio": True, "video": False},
        async_processing=True,
    )

    if webrtc_ctx.audio_receiver:
        audio_frames = []
        try:
            while True:
                audio_frame = webrtc_ctx.audio_receiver.get(timeout=1)
                audio_frames.append(audio_frame.to_ndarray().flatten())
        except queue.Empty:
            pass

        if audio_frames:
            audio_np = np.concatenate(audio_frames)
            sample_rate = 48000

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                write(tmpfile.name, sample_rate, audio_np.astype(np.int16))
                temp_audio_path = tmpfile.name

            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_audio_path) as source:
                audio_data = recognizer.record(source)
                try:
                    transcribed_text = recognizer.recognize_google(audio_data)
                    st.success(f"🗣️ You said: {transcribed_text}")
                    text_input = transcribed_text
                except sr.UnknownValueError:
                    st.error("❌ Could not understand audio.")
                except sr.RequestError as e:
                    st.error(f"❌ Speech recognition error: {e}")

# 📝 Manual Text Input
typed_input = st.text_input("💬 Or type your question:")
if typed_input:
    text_input = typed_input

# 🤖 Answer Logic
if text_input:
    st.session_state.chat_history.append(("You", text_input))

    best_match = None
    best_score = 0.0
    for q, a in faq_qa:
        score = similarity(text_input, q)
        if score > best_score:
            best_score = score
            best_match = (q, a)

    if best_score > 0.6:
        answer = f"**Q:** {best_match[0]}\n\n**🧠 Nova says:** {best_match[1]}"
    else:
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are Nova, a helpful AI FAQ assistant."},
                    {"role": "user", "content": text_input}
                ]
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            answer = f"❌ GPT failed: {e}"

    st.session_state.chat_history.append(("Nova", answer))

# 💬 Show Chat
st.markdown("## 💬 Chat History")
for role, message in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑‍💻 You:** {message}")
    else:
        st.markdown(f"**🤖 Nova:** {message}")
