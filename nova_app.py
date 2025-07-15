import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from difflib import SequenceMatcher
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import tempfile

# 🎯 Together AI setup
api_key = st.secrets["together"]["api_key"]
client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# 📁 Load FAQ CSV
FAQ_FILE = "faqs.csv"
if not os.path.exists(FAQ_FILE):
    st.error("🚨 'faqs.csv' not found in app folder.")
    st.stop()

df = pd.read_csv(FAQ_FILE)
faq_qa = list(zip(df["Question"].astype(str), df["Answer"].astype(str)))

# 🎨 App config
st.set_page_config(page_title="Nova - Smart FAQ Assistant", page_icon="🤖")

# 📸 Sidebar
with st.sidebar:
    try:
        st.image("nova_bot.png", use_container_width=True)
    except:
        st.warning("🖼️ 'nova_bot.png' not found.")
    st.markdown("### Built by **Solace** & **Nyx** ✨")
    st.markdown("💬 Ask anything from your FAQ. If not found, Nova asks GPT!")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []

# 💬 Chat history init
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🧠 Title and input
st.title("🤖 Nova - Smart FAQ Assistant")
st.markdown("Type your question or use the microphone 🎤")

# 🎤 Microphone input
audio = mic_recorder(start_prompt="🎤 Click to speak", stop_prompt="⏹️ Stop", key="mic", use_container_width=True)

user_question = st.text_input("💬 Or type your question:")

if audio:
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio["bytes"])
        temp_audio_path = temp_audio.name

    with sr.AudioFile(temp_audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            user_question = recognizer.recognize_google(audio_data)
            st.success(f"🎤 You said: {user_question}")
        except sr.UnknownValueError:
            st.warning("❗ Sorry, I couldn't understand your speech.")
        except sr.RequestError:
            st.error("❌ Speech recognition service failed.")

# 🔍 Process question
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
        st.success(f"✅ Matched FAQ (Similarity: {best_score:.2f})")
        st.markdown(f"**Q:** {best_match[0]}")
        st.markdown(f"**🧠 Nova says:** {best_match[1]}")
        st.session_state.chat_history.append((user_question, best_match[1]))
    else:
        st.info("🤔 No FAQ match. Asking GPT...")
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are Nova, a helpful AI FAQ assistant."},
                    {"role": "user", "content": user_question}
                ]
            )
            answer = response.choices[0].message.content.strip()
            st.markdown("**🤖 Nova says:**")
            st.info(answer)
            st.session_state.chat_history.append((user_question, answer))
        except Exception as e:
            st.error("❌ GPT failed to respond.")
            st.exception(e)

# 📜 Chat History Display
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### 🗂️ Previous Q&A")
    for i, (q, a) in enumerate(reversed(st.session_state.chat_history[-10:]), 1):
        st.markdown(f"**Q{i}:** {q}")
        st.markdown(f"**A{i}:** {a}")
