import streamlit as st
from dotenv import load_dotenv
import os
import requests
from PIL import Image

# Load .env file
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Set page config
st.set_page_config(page_title="Nova - GPT FAQ Assistant", layout="wide")

# Check for API key
if not api_key:
    st.error("❌ OPENROUTER_API_KEY not found in .env file.")
    st.stop()

# Load Nova image
if os.path.exists("nova_bot.png"):
    nova_img = Image.open("nova_bot.png")
else:
    st.error("❌ nova_bot.png not found in the project folder.")
    st.stop()

# Custom dark mode toggle
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=True)

# Apply Dark Mode Styles
if dark_mode:
    st.markdown("""
        <style>
            .stApp {
                background-color: #121212;
                color: #FFFFFF;
            }
            section[data-testid="stSidebar"] {
                background-color: #1E1E1E !important;
                color: #FFFFFF !important;
            }
            .stChatMessage {
                background-color: #121212 !important;
                color: #DDD !important;
            }
            .stMarkdown {
                color: #DDD !important;
            }
            textarea {
                background-color: #2A2A2A !important;
                color: #FFFFFF !important;
            }
            div[data-testid="stChatInput"] textarea {
                background-color: #2A2A2A !important;
                color: white !important;
                border: 1px solid #555 !important;
                border-radius: 8px;
            }
            div[data-testid="stChatInput"] button {
                background-color: #444 !important;
                color: white !important;
                border: 1px solid #888 !important;
                border-radius: 6px;
            }
            .stButton > button {
                background-color: #333 !important;
                color: white !important;
                border: 1px solid #555 !important;
            }
            .stRadio > div, .stToggle {
                background-color: #2A2A2A !important;
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)

# Sidebar: Nova mood selector
st.sidebar.image(nova_img, width=100)
mood = st.sidebar.radio("🧠 Pick Nova's Mood", ["Professional", "Friendly", "Sassy 😎", "Minimal"])

# Title and description
st.title("💬 Nova - GPT FAQ Assistant")
st.caption(f"Ask me anything, honey 🍯 I'm powered by GPT. ({mood} mode)")

# Chat input
user_query = st.chat_input("What would you like to ask?")

# Display past chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if user_query:
    st.chat_message("user").markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    system_prompt = {
        "Professional": "You are a polite and informative assistant.",
        "Friendly": "You are a cheerful and helpful assistant.",
        "Sassy 😎": "You are a witty assistant with sass but still helpful.",
        "Minimal": "Give very short, precise answers."
    }[mood]

    payload = {
        "model": "openchat/openchat-3.5-1210",
        "messages": [
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
        ]
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        ai_msg = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        ai_msg = f"❌ Error contacting Nova's brain: {e}"

    with st.chat_message("assistant"):
        st.markdown(ai_msg)

    st.session_state.messages.append({"role": "assistant", "content": ai_msg})
