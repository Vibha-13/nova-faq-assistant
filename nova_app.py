import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from difflib import SequenceMatcher
from streamlit_audio_recorder import audio_recorder
import tempfile
import speech_recognition as sr

# API Key
api_key = st.secrets["together"]["api_key"]
client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# Load FAQ
FAQ_FILE = "faqs.csv"
if not os.path.exists(FAQ_FILE):
    st.error("❌ 'faqs.csv' not found.")
    st.stop()

df = pd.read_csv(FAQ_FILE)
faq_qa = list(zip(df["Question"].astype(str), df["Answer"].astype(str)))

# Page config
st.set_page_config(page_title="Nova - Smart FAQ Assistant", page_icon="🤖")

# Sidebar
with st.sidebar:
    st.image("nova_bot.png", use_container_width=True, caption="Nova, your smart assistant 🤖")
    st.markdown("### Built by **Solace** & **Nyx** ✨")
    st.markdown("---")
    st.button("🗑️ Clear Chat", on_click=lambda: st.session_state.update({"chat_history": []}))

# Init chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Title + Voice Input
st.title("🤖 Nova - Smart FAQ Assistant")
st.markdown("Type your question or use the microphone 🎤")

audio_bytes = audio_recorder(text="🎙️ Speak your question...", icon_size="2x")
voice_input = ""

if audio_bytes:
    try:
        recognizer = sr.Recognizer()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(audio_bytes["bytes"])
            temp_path = temp_audio_file.name

        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)
            voice_input = recognizer.recognize_google(audio_data)

        st.success(f"🗣️ You said: {voice_input}")
    except Exception as e:
        st.error("❌ Failed to process audio input.")
        st.exception(e)

# Text input
user_input = st.text_input("💬 Or type your question:", value=voice_input)

if user_input:
    def similarity(a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    best_match = None
    best_score = 0.0
    for q, a in faq_qa:
        score = similarity(user_input, q)
        if score > best_score:
            best_score = score
            best_match = (q, a)

    if best_score > 0.6:
        answer = best_match[1]
        st.success("✅ Nova found a relevant answer!")
        st.markdown(f"**Q:** {best_match[0]}")
        st.markdown(f"**🧠 Nova says:** {answer}")
    else:
        st.warning("🤔 No close FAQ match. Asking GPT...")
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are Nova, a helpful FAQ assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response.choices[0].message.content.strip()
            st.info(answer)
        except Exception as e:
            st.error("❌ GPT API failed.")
            st.exception(e)

    # Save chat history
    st.session_state.chat_history.append({"question": user_input, "answer": answer})

# Show chat history
if st.session_state.chat_history:
    st.markdown("## 📜 Chat History")
    for chat in reversed(st.session_state.chat_history[-5:]):
        st.markdown(f"**Q:** {chat['question']}")
        st.markdown(f"**A:** {chat['answer']}")
