import streamlit as st
from dotenv import load_dotenv
import os
import requests
import json
import random

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Config file for persistent memory
CONFIG_FILE = "nova_config.json"

# Load saved config if exists
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
else:
    config = {"user_name": "Solace", "nova_mood": "Friendly"}  # Default values

# Streamlit page config
st.set_page_config(page_title="Nova - GPT FAQ Assistant", layout="centered", initial_sidebar_state="expanded")

# Custom CSS for Nova theme
def inject_custom_css(dark_mode):
    if dark_mode:
        background = "#121212"
        text_color = "#ffffff"
        bubble_color = "#2A2A2A"
    else:
        background = "#f5f5f5"
        text_color = "#000000"
        bubble_color = "#e6e6e6"

    st.markdown(f"""
        <style>
            .stApp {{
                background-color: {background};
                color: {text_color};
            }}
            .message-bubble {{
                padding: 1rem;
                border-radius: 10px;
                margin: 0.5rem 0;
                background-color: {bubble_color};
            }}
            .nova-bubble {{
                background-color: #DAD4E0;
            }}
            .user-bubble {{
                background-color: #ccc;
            }}
            .chat-icon {{
                font-size: 1.2rem;
                margin-right: 5px;
            }}
        </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    image_path = "assets/nova_bot.png"
    if os.path.exists(image_path):
        st.image(image_path, width=200)
    else:
        st.error("❌ nova_bot.png not found in 'assets/' folder.")

    # Name input
    config["user_name"] = st.text_input("👤 Your Name:", value=config.get("user_name", "Solace"))

    # Mood selector
    st.markdown("## 🧠 Pick Nova's Mood")
    config["nova_mood"] = st.radio(
        "",
        ("Professional", "Friendly", "Sassy 😎", "Minimal"),
        index=("Professional", "Friendly", "Sassy 😎", "Minimal").index(config.get("nova_mood", "Friendly"))
    )

    # Dark mode toggle
    dark_mode = st.toggle("🌗 Dark Mode", value=False)

    inject_custom_css(dark_mode)

    # Clear chat
    st.markdown("---")
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []

# Save updated config
with open(CONFIG_FILE, "w") as f:
    json.dump(config, f)

# Mood prompts
tone_dict = {
    "Professional": f"You are Nova, a knowledgeable assistant who provides concise, expert-level answers professionally.",
    "Friendly": f"You are Nova, a warm and friendly assistant who calls {config['user_name']} by name and explains things in a kind manner.",
    "Sassy 😎": f"You're Nova, a sassy, witty assistant who calls {config['user_name']} by name, uses humor, emojis, and playful banter. Keep it fun but accurate.",
    "Minimal": f"You're Nova. Greet {config['user_name']} shortly and answer in ultra-brief style with no fluff."
}
tone_prefix = tone_dict[config["nova_mood"]]

# Emoji reactions
sass_emojis = ["😏", "💅", "🤖", "✨", "🔥", "🚀", "🦾"]

# GPT API call
def call_openrouter_gpt(prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    mood = config["nova_mood"]
    # Add playful reaction if sassy
    if mood == "Sassy 😎":
        prompt += f"\n\n(End response with a random playful emoji like {random.choice(sass_emojis)})"

    payload = {
        "model": "openai/gpt-3.5-turbo",
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

# Main chat UI
st.markdown("## 💬 Nova - GPT FAQ Assistant")
st.markdown(f"Hey {config['user_name']} 👋, I'm Nova! Ask me anything, honey 🍯\n")

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Initial greeting
    st.session_state.messages.append({"role": "assistant", "content": f"Hi {config['user_name']}! Ready to get started? {random.choice(sass_emojis) if config['nova_mood']=='Sassy 😎' else ''}"})

# Render previous chat
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        st.markdown(f"""<div class="message-bubble user-bubble">🧍‍♂️ <b>You:</b> {content}</div>""", unsafe_allow_html=True)
    elif role == "assistant":
        st.markdown(f"""<div class="message-bubble nova-bubble">🧠 <b>Nova:</b> {content}</div>""", unsafe_allow_html=True)

# Chat input
user_query = st.chat_input("Ask your question:")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.markdown(f"""<div class="message-bubble user-bubble">🧍‍♂️ <b>You:</b> {user_query}</div>""", unsafe_allow_html=True)

    with st.spinner("Nova is thinking... ⌛"):
        reply = call_openrouter_gpt(user_query)

        # Fun idle comment chance
        if random.random() < 0.2 and config["nova_mood"] == "Sassy 😎":
            reply += f"\n\nP.S. {config['user_name']}, you ask the best questions 😎"

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.markdown(f"""<div class="message-bubble nova-bubble">🧠 <b>Nova:</b> {reply}</div>""", unsafe_allow_html=True)
