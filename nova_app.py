import streamlit as st
from streamlit_chat import message
import time

# ---------------------- Config & Style ----------------------
st.set_page_config(page_title="Nova - FAQ Assistant", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #fdf6ff;
        font-family: 'Segoe UI', sans-serif;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
        padding: 8px;
    }
    .stButton>button {
        background-color: #ff69b4;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Nova Mood Styles ----------------------
MOOD_STYLES = {
    "friendly": "🧠 Nova (Friendly):",
    "sassy": "💅 Nova (Sassy):",
    "professional": "💼 Nova (Pro):",
    "flirty": "😉 Nova (Flirty):"
}

# ---------------------- Session State Setup ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------- Generate Nova Reply ----------------------
def generate_nova_reply(user_msg, mood):
    msg = user_msg.lower()

    # Specific, helpful replies
    if "generate pictures" in msg or "image generation" in msg or "ai for images" in msg:
        return "🎨 For image generation, top AIs are **DALL·E**, **Midjourney**, and **Stable Diffusion**."

    elif "best ai" in msg and "text" in msg:
        return "✍️ GPT-4 (like me!) is considered the best for generating human-like text."

    elif "nova" in msg:
        return "Nova is your personal AI FAQ assistant, full of brains and attitude 💅"

    elif "python" in msg:
        return "🐍 Python is a beginner-friendly language perfect for AI, automation, and web development."

    elif "network" in msg or "networking" in msg:
        return "🌐 Networking means connecting devices so they can share data. Like a group chat for computers!"

    elif "machine learning" in msg or "ml" in msg:
        return "🧠 Machine learning teaches systems to learn from data — like how Nova learns *your vibe* 😉"

    elif "love" in msg:
        return "Awww 🥹 Nova loves you back, Captain 💖"

    # Catch-all fallback
    return f"{MOOD_STYLES.get(mood, '🤖')} You asked: *{user_msg}*"

# ---------------------- Header ----------------------
st.title("🧠 Nova - Your FAQ Assistant")
st.markdown("Ask me anything about your project. Nova’s got brains and personality 😎")

# ---------------------- Mood Picker ----------------------
mood = st.selectbox("Choose Nova’s Mood", options=["friendly", "sassy", "professional", "flirty"], index=0)

# ---------------------- Input ----------------------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 Ask your question:", key="input", placeholder="e.g. What is machine learning?")
    submit = st.form_submit_button("Send")

# ---------------------- Processing ----------------------
if submit and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "text": user_input})

    # Generate Nova's reply
    response = generate_nova_reply(user_input, mood)

    # Simulate typing
    st.session_state.messages.append({"role": "nova", "text": response})

# ---------------------- Display Messages ----------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        message(msg["text"], is_user=True, key=msg["text"] + "_user")
    else:
        message(msg["text"], key=msg["text"] + "_nova")

