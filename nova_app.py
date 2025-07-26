import streamlit as st
from dotenv import load_dotenv
import os
import requests

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Set page config
st.set_page_config(page_title="Nova - GPT FAQ Assistant", layout="centered", initial_sidebar_state="expanded")

# ----------------------- Sidebar -----------------------
with st.sidebar:
    st.image("assets/nova_bot.png", width=200)
    st.markdown("## 🧠 Pick Nova's Mood")
    mood = st.radio(
        "",
        ("Professional", "Friendly", "Sassy 😎", "Minimal"),
        index=1
    )
    
    st.markdown("## 🌓 Theme Toggle")
    # -- Dark Mode Toggle --
    dark_mode = st.toggle("🌗 Dark Mode", value=False)

    st.markdown("---")
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []

# ------------------ Dark Mode Styling ------------------
if dark_mode:
    st.markdown("""
        <style>
            .stApp {
                background-color: #121212;
                color: #FFFFFF;
            }
            .css-1cpxqw2, .css-ffhzg2, .css-1d391kg {
                background-color: #1E1E1E !important;
                color: white !important;
            }
            .stTextInput > div > div > input {
                background-color: #2A2A2A !important;
                color: white !important;
            }
            .stButton button {
                background-color: #333 !important;
                color: white !important;
                border: 1px solid #555 !important;
            }
            .stRadio > div {
                background-color: #2A2A2A !important;
                color: white !important;
                border-radius: 8px;
            }
            .stMarkdown, .stChatMessage {
                color: #ddd !important;
            }
            textarea {
                background-color: #2A2A2A !important;
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)

# ------------------ Tone/Mood System Prompt ------------------
tone_dict = {
    "Professional": "You are Nova, a knowledgeable assistant who provides concise, expert-level answers in a professional tone.",
    "Friendly": "You are Nova, a warm and friendly assistant who explains things in an easy and kind manner.",
    "Sassy 😎": "You're Nova, a sassy, witty assistant who serves answers with humor and flair. Keep it fun but accurate.",
    "Minimal": "You're Nova. Keep answers extremely short, to the point, with no fluff."
}
tone_prefix = tone_dict[mood]

# ------------------ GPT Function ------------------
def call_openrouter_gpt(prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",  # Update as needed
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

# ------------------ Chat Interface ------------------
st.markdown("## 💬 Nova - GPT FAQ Assistant")
st.markdown("Ask me anything, honey 🍯 I'm powered by GPT.\n")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past chats
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_query = st.chat_input("Ask your question:")

if user_query:
    st.chat_message("user").markdown(f"👤 You: {user_query}")
    st.session_state.messages.append({"role": "user", "content": f"👤 You: {user_query}"})

    with st.chat_message("assistant"):
        with st.spinner("Nova is thinking..."):
            gpt_reply = call_openrouter_gpt(user_query)
            st.markdown(f"🧠 Nova: {gpt_reply}")
            st.session_state.messages.append({"role": "assistant", "content": f"🧠 Nova: {gpt_reply}"})
