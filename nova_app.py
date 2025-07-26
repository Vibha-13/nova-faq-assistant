import streamlit as st
import os
import requests

# --- App Config ---
st.set_page_config(page_title="Nova - GPT FAQ Assistant", page_icon="💬", layout="centered")

# --- Dark Mode Toggle ---
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)

if dark_mode:
    st.markdown("""
        <style>
            body, .stApp {
                background-color: #1e1e1e;
                color: #f1f1f1;
            }
            .stTextInput > div > input, .stTextArea textarea, .stChatInput input {
                background-color: #2c2c2c;
                color: white;
                border: 1px solid #555;
            }
            .stButton button {
                background-color: #333 !important;
                color: white !important;
            }
            .stRadio > div {
                background-color: #2a2a2a;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            .stMarkdown h1, .stMarkdown h2 {
                color: #e6e6e6;
            }
            .stChatMessage {
                background-color: #262626;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

# --- Sidebar Branding ---
st.sidebar.title("🧠 Pick Nova's Mood")
mood = st.sidebar.radio("", ["Professional", "Friendly", "Sassy 😎", "Minimal"])

# --- Load Nova Avatar ---
image_path = "assets/nova_bot.png"
if os.path.exists(image_path):
    st.image(image_path, width=200)
else:
    st.error("❌ `nova_bot.png` not found in /assets folder!")

# --- Title ---
st.title("💬 Nova - GPT FAQ Assistant")

# --- Mood Greetings ---
mood_greetings = {
    "Professional": "Ask me anything. I'm your knowledge assistant.",
    "Friendly": "Ask me anything, buddy 👋",
    "Sassy 😎": "Ask me anything, honey 🍯 I'm powered by GPT.",
    "Minimal": ""
}
st.markdown(f"**{mood_greetings[mood]}**")

# --- User Input ---
user_question = st.text_input("What do you want to ask?")

# --- Handle User Input ---
if user_question:
    with st.spinner("Thinking... 🧠"):
        try:
            headers = {
                "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "openchat/openchat-3.5-0106",
                "messages": [
                    {"role": "system", "content": "You're Nova, a helpful AI assistant with the mood: " + mood},
                    {"role": "user", "content": user_question}
                ]
            }
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            reply = response.json()['choices'][0]['message']['content']
            st.markdown(f"**Nova says:** {reply}")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error contacting Nova's brain: {e}")
