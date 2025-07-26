import streamlit as st
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

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
                background-color: #f7f0ff;
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
    # Image
    image_path = "assets/nova_bot.png"
    if os.path.exists(image_path):
        st.image(image_path, width=200)
    else:
        st.error("❌ nova_bot.png not found in 'assets/' folder.")

    # Mood selector
    st.markdown("## 🧠 Pick Nova's Mood")
    mood = st.radio(
        "",
        ("Professional", "Friendly", "Sassy 😎", "Minimal"),
        index=1
    )

    # Dark mode toggle
    dark_mode = st.toggle("🌗 Dark Mode", value=False)

    # Inject styling
    inject_custom_css(dark_mode)

    # Clear button
    st.markdown("---")
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []

# Mood system prompts
tone_dict = {
    "Professional": "You are Nova, a knowledgeable assistant who provides concise, expert-level answers in a professional tone.",
    "Friendly": "You are Nova, a warm and friendly assistant who explains things in an easy and kind manner.",
    "Sassy 😎": "You're Nova, a sassy, witty assistant who serves answers with humor and flair. Keep it fun but accurate.",
    "Minimal": "You're Nova. Keep answers extremely short, to the point, with no fluff."
}
tone_prefix = tone_dict[mood]

# OpenRouter API call
def call_openrouter_gpt(prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",  # or openchat/openchat-3.5-0106
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

# Main chat title
st.markdown("## 💬 Nova - GPT FAQ Assistant")
st.markdown("Ask me anything, honey 🍯 I'm powered by GPT.\n")

# Chat session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous chat
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        st.markdown(f"""<div class="message-bubble user-bubble">🧍‍♂️ <b>You:</b> {content}</div>""", unsafe_allow_html=True)
    elif role == "assistant":
        st.markdown(f"""<div class="message-bubble nova-bubble">🧠 <b>Nova:</b> {content}</div>""", unsafe_allow_html=True)

# Input
user_query = st.chat_input("Ask your question:")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.markdown(f"""<div class="message-bubble user-bubble">🧍‍♂️ <b>You:</b> {user_query}</div>""", unsafe_allow_html=True)

    with st.spinner("Nova is thinking..."):
        reply = call_openrouter_gpt(user_query)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.markdown(f"""<div class="message-bubble nova-bubble">🧠 <b>Nova:</b> {reply}</div>""", unsafe_allow_html=True)
