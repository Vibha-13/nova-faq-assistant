import streamlit as st
import requests
from PIL import Image

# Title and icon
st.set_page_config(page_title="Nova GPT FAQ Assistant", page_icon="🤖")

# Load bot image in sidebar
with st.sidebar:
    st.image("assets/nova_bot.png", width=200)
    st.title("✨ Nova GPT FAQ Assistant")
    mood = st.selectbox("Choose Nova's Mood 💫", ["Friendly", "Professional", "Sassy"])
    st.markdown("---")
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []

# System prompt based on mood
system_messages = {
    "Friendly": "You're Nova, a warm, friendly, emoji-using AI who answers questions helpfully and with a smile. Keep it light and cute!",
    "Professional": "You're Nova, a calm, professional assistant that explains concepts clearly and concisely.",
    "Sassy": "You're Nova, a bold and sassy assistant who gives answers with confidence and flair, with a sprinkle of sarcasm when needed."
}

# Set up OpenRouter API key (stored safely in secrets or env var)
API_KEY = st.secrets.get("OPENROUTER_API_KEY", "your-api-key-here")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat UI
st.title("💬 Chat with Nova!")
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Add user message to history
    st.session_state.chat_history.append(("user", user_input))

    # Build full chat messages
    messages = [{"role": "system", "content": system_messages[mood]}]
    for sender, msg in st.session_state.chat_history:
        role = "user" if sender == "user" else "assistant"
        messages.append({"role": role, "content": msg})

    # Prepare request payload
    payload = {
        "model": "openai/gpt-3.5-turbo",  # or openrouter/gpt-4
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 300
    }

    # Send request to OpenRouter
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        nova_reply = response.json()["choices"][0]["message"]["content"]
    else:
        nova_reply = "Oops! Nova hit a snag. Please try again."

    # Add Nova's reply to chat history
    st.session_state.chat_history.append(("nova", nova_reply))

# Display chat history
for sender, msg in st.session_state.chat_history:
    if sender == "user":
        with st.chat_message("user"):
            st.markdown(msg)
    else:
        with st.chat_message("assistant"):
            st.markdown(msg)
