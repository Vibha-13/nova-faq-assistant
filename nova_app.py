import streamlit as st
import os
from dotenv import load_dotenv
import requests

# Load .env file
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Basic Streamlit page config
st.set_page_config(page_title="Nova - GPT FAQ Assistant", page_icon="🧠", layout="centered")

# Dark mode toggle
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=True)
if dark_mode:
    st.markdown("""
        <style>
        body { background-color: #0e1117; color: white; }
        .stTextInput>div>div>input { background-color: #262730; color: white; }
        </style>
    """, unsafe_allow_html=True)

# Sidebar logo
img_path = os.path.join("assets", "nova_bot.png")
if os.path.exists(img_path):
    st.sidebar.image(img_path, width=150, caption="Nova Assistant 🤖")
else:
    st.sidebar.warning("nova_bot.png not found in /assets")

st.sidebar.markdown("---")
mood = st.sidebar.radio("🧠 Pick Nova's Mood", ["Professional", "Friendly", "Sassy 😎", "Minimal"])
if mood == "Sassy 😎":
    tone_prefix = "You are a bold, cheeky assistant who answers FAQs with sass and humor."
elif mood == "Friendly":
    tone_prefix = "You are a helpful and cheerful assistant who explains things in a kind, friendly way."
elif mood == "Minimal":
    tone_prefix = "Answer concisely. Avoid extra chatter. Minimal tone."
else:
    tone_prefix = "You are a professional AI assistant designed to answer technical FAQs clearly."

# Title and intro
st.markdown("### 💬 Nova - GPT FAQ Assistant")
st.markdown("Ask me anything, honey 🍯 I'm powered by GPT.")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("Ask your question here...")

# Clear button
if st.sidebar.button("🧹 Clear Conversation"):
    st.session_state.chat_history = []
    st.rerun()

# Function to call OpenRouter GPT
def call_openrouter_gpt(prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openrouter/openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": tone_prefix},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Error contacting Nova's brain: {e}"

# Process user input
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Nova is typing..."):
        reply = call_openrouter_gpt(user_input)
        st.session_state.chat_history.append(("nova", reply))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.chat_message("user").markdown(message)
    else:
        st.chat_message("assistant").markdown(message)
