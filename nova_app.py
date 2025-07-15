import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from difflib import SequenceMatcher
from streamlit_audio_recorder import audio_recorder
import base64
import tempfile
import speech_recognition as sr

# 🎯 API Setup
api_key = st.secrets["together"]["api_key"]
client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# 📁 Check for FAQ file
FAQ_FILE = "faqs.csv"
if not os.path.exists(FAQ_FILE):
    st.error("🚨 FAQ file not found! Please ensure 'faqs.csv' is in the app folder.")
    st.stop()

# 📚 Load FAQs
df = pd.read_csv(FAQ_FILE)
faq_qa = list(zip(df["Question"].astype(str), df["Answer"].astype(str)))

# 🎨 Page Config
st.set_page_config(page_title="Nova - Smart FAQ Assistant", page_icon="🤖")

# 💬 Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 📸 Sidebar
with st.sidebar:
    st.image("nova_bot.png", caption="Nova, your smart assistant 🤖", use_container_width=True)
    st.markdown("### Built by **Solace** & **Nyx** ✨")
    st.markdown("---")
    st.markdown("💡 Nova answers from your FAQ. If unsure, she asks GPT!")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []

# 🧠 Title + Description
st.title("🤖 Nova - Smart FAQ Assistant")
st.markdown("#### Ask anything from the loaded FAQ file 📄")

# 📥 Input Section
text_input = st.text_input("💬 Ask your question:")

# 🎙️ Voice Input
with st.expander("🎤 Or click here to speak"):
    audio_bytes = audio_recorder()
    if audio_bytes:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_bytes)
            temp_audio_path = f.name

        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = recognizer.record(source)
            try:
                transcribed_text = recognizer.recognize_google(audio_data)
                st.success(f"🗣️ You said: {transcribed_text}")
                text_input = transcribed_text  # Auto-trigger
            except sr.UnknownValueError:
                st.error("❌ Could not understand your speech.")
            except sr.RequestError as e:
                st.error(f"❌ Error from Google Speech API: {e}")

user_question = text_input.strip()

# 🔍 Match FAQ or Ask GPT
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
        st.success(f"✅ Found a FAQ match! (Similarity: {best_score:.2f})")
    else:
        st.warning("🤔 No exact FAQ match found. Asking GPT...")
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are Nova, a helpful AI FAQ assistant who answers clearly and positively."},
                    {"role": "user", "content": user_question}
                ]
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            st.error("❌ GPT failed to respond. Here's the error:")
            st.exception(e)
            answer = None

    if answer:
        # 🧠 Show answer + Save history
        st.markdown("**🤖 Nova says:**")
        st.info(answer)
        st.session_state.chat_history.append((user_question, answer))

# 💬 Chat History
if st.session_state.chat_history:
    with st.expander("📜 Previous Q&A"):
        for q, a in reversed(st.session_state.chat_history):
            st.markdown(f"**🧍 You:** {q}")
            st.markdown(f"**🤖 Nova:** {a}")
            st.markdown("---")
