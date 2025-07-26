import streamlit as st
import requests
import os
from dotenv import load_dotenv
from PIL import Image

# Load API Key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Page config
st.set_page_config(page_title="Nova - GPT FAQ Assistant", layout="centered")

# ---- DARK MODE TOGGLE ----
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

mode = st.toggle("🌗 Toggle Dark Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = mode

if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
        body { background-color: #0e1117; color: #ffffff; }
        .stApp { background-color: #0e1117; color: white; }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body { background-color: #f8f9fa; color: #000000; }
        .stApp { background-color: #f8f9fa; color: black; }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---- SIDEBAR ----
st.sidebar.title("🧠 Pick Nova's Mood")
persona = st.sidebar.radio("Choose Nova's personality:", ["Professional", "Friendly", "Sassy 😎", "Minimal"])

# ---- HEADER ----
st.markdown("## 💬 Nova - GPT FAQ Assistant")
st.caption("Ask me anything, honey 🍯 I'm powered by GPT.")

# ---- IMAGE LOADING ----
image_path = "assets/nova_bot.png"
if os.path.exists(image_path):
    st.image(image_path, width=200)
else:
    st.error("❌ nova_bot.png not found in the project folder.")

# ---- USER QUERY ----
question = st.text_input("Type your question here:")

# ---- RESPONSE ----
if question and API_KEY:
    with st.spinner("Thinking... 💭"):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        prompt_map = {
            "Professional": "Answer in a clear, expert tone.",
            "Friendly": "Answer casually like a helpful friend.",
            "Sassy 😎": "Answer with a sassy, witty twist.",
            "Minimal": "Answer in the shortest and clearest way possible."
        }

        body = {
            "model": "openchat/openchat-3.5-0106",
            "messages": [
                {"role": "system", "content": prompt_map[persona]},
                {"role": "user", "content": question}
            ]
        }

        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers)
            res.raise_for_status()
            answer = res.json()["choices"][0]["message"]["content"]
            st.success(answer)
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error contacting Nova's brain: {e}")
else:
    if not API_KEY:
        st.warning("🔑 Please set your OpenRouter API key in the `.env` file.")
