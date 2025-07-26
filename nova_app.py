import streamlit as st
import requests
import os
from PIL import Image

# Load logo if available
if os.path.exists("nova_bot.png"):
    st.image("nova_bot.png", width=120)

st.markdown("<h1 style='text-align: center;'>🧠 Nova - Your FAQ Assistant</h1>", unsafe_allow_html=True)
st.markdown("#### Ask anything related to your project. Nova answers with brains and vibe 💫")

# Sidebar for mood
st.sidebar.title("🎭 Nova's Mood")
mood = st.sidebar.radio("Choose Nova’s mode", ("friendly", "professional", "funny"))

# Clear chat button
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat_history = []

# Form for user input
with st.form("chat_input", clear_on_submit=True):
    user_input = st.text_input("💬 Type your question:")
    submitted = st.form_submit_button("Send")

# System messages based on mood
system_messages = {
    "friendly": "You are Nova, a warm and friendly assistant. Reply with kindness and sprinkle emojis.",
    "professional": "You are Nova, a professional assistant who gives clear and concise project answers.",
    "funny": "You are Nova, a witty assistant who answers with humor but still helpful."
}

# Function to get response from OpenRouter API
def get_nova_reply(prompt, mood):
    try:
        headers = {
            "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-3.5-turbo",  # or gpt-4 if you have access
            "messages": [
                {"role": "system", "content": system_messages[mood]},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 300
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"⚠️ Nova broke a wire: {str(e)}"

# Chat logic
if submitted and user_input:
    st.session_state.chat_history.append(("user", user_input))
    nova_reply = get_nova_reply(user_input, mood)
    st.session_state.chat_history.append(("nova", nova_reply))

# Display chat
for sender, msg in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"👤 **You:** {msg}")
    else:
        st.markdown(f"🧠 **Nova:** {msg}")
