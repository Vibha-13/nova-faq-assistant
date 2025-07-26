import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(
    page_title="Nova - GPT FAQ Assistant",
    layout="centered",
    initial_sidebar_state="expanded",
    page_icon="🌟"
)

# 🚀 Inject toggleable light/dark theme, typed animation, and calling JS
st.markdown("""
<script>
    function typeText(txt, containerId) {
        const container = document.getElementById(containerId);
        container.innerHTML = '';
        let i = 0;
        function type() {
            if (i < txt.length) {
                container.innerHTML += txt.charAt(i);
                i++;
                setTimeout(type, 25);
            }
        }
        type();
    }
    function scrollToBottom() {
        const c = document.getElementById('chat-container');
        c.scrollTop = c.scrollHeight;
    }
</script>

<style>
:root {
    --bg-light: #ffffff;
    --text-light: #222;
    --bg-dark: #121212;
    --text-dark: #eee;
    --nova-light: #ede7f6;
    --nova-dark: #2a2a3f;
    --user-light: #dadada;
    --user-dark: #3a3a4d;
}
body.light {
    background-color: var(--bg-light);
    color: var(--text-light);
}
body.dark {
    background-color: var(--bg-dark);
    color: var(--text-dark);
}
.user-bubble {
    border-radius: 10px;
    padding: 8px;
    margin: 6px 0;
}
.nova-bubble {
    border-radius: 10px;
    padding: 8px;
    margin: 6px 0;
}
.light .user-bubble { background: var(--user-light); color: var(--text-light); }
.light .nova-bubble { background: var(--nova-light); color: var(--text-light); }
.dark .user-bubble { background: var(--user-dark); color: var(--text-dark); }
.dark .nova-bubble { background: var(--nova-dark); color: var(--text-dark); }
.mood-btn {
    margin: 3px;
    padding: 4px 8px;
    border: 1px solid transparent;
    cursor: pointer;
    border-radius: 6px;
}
.mood-btn.selected {
    border-color: #7f5af0;
    background: rgba(127,90,240,0.2);
}
#chat-container {
    max-height: 500px;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

# Sidebar: favicon + image
st.sidebar.image("assets/nova_bot.png", width=120)
st.sidebar.markdown("## 🧠 Nova Assistant")
moods = ["Professional", "Friendly", "Sassy 😎", "Minimal"]

# Theme
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
dm = st.sidebar.checkbox("🌗 Dark Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = dm

# Mood picker
st.sidebar.markdown("## 🎭 Nova's Mood")
for m in moods:
    if st.sidebar.button(m, key=m):
        st.session_state.mood = m
if "mood" not in st.session_state:
    st.session_state.mood = "Friendly"

# Clear chat
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []

# Inject body class for theme
body_class = "dark" if dm else "light"
st.markdown(f'<script>document.body.className = "{body_class}";</script>', unsafe_allow_html=True)

# Mapping system prompt
tone = {
    "Professional": "You are a concise, professional assistant.",
    "Friendly": "You are friendly and helpful with emojis.",
    "Sassy 😎": "Sassy witty assistant with flair.",
    "Minimal": "Keep answers extremely short and to the point."
}[st.session_state.mood]

# Header
st.markdown(f"# 💬 Nova — GPT FAQ Assistant")
st.caption("Ask anything — Nova is ready to shine! ✨")

# Chat container
chat_container = st.container()
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat
chat_container.markdown('<div id="chat-container"></div>', unsafe_allow_html=True)

for idx, msg in enumerate(st.session_state.messages):
    role, text = msg
    bubble = "user-bubble" if role=="user" else "nova-bubble"
    prefix = "👤 You:" if role=="user" else "🧠 Nova:"
    chat_container.markdown(f'<div class="{bubble}">{prefix} {text}</div>', unsafe_allow_html=True)

# Input
user_input = st.text_input("Type your question here...")

if user_input:
    st.session_state.messages.append(("user", user_input))
    chat_container.markdown(f'<div class="user-bubble">👤 You: {user_input}</div>', unsafe_allow_html=True)

    with st.spinner("Nova is thinking..."):
        payload = {
            "model": "openrouter/openai/gpt-3.5-turbo",
            "messages": [
                {"role":"system","content":tone},
                {"role":"user","content":user_input}
            ]
        }
        headers = {"Authorization":f"Bearer {API_KEY}"}
        try:
            resp = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            nova = resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            nova = f"Error: {e}"

    st.markdown(f'<div class="nova-bubble" id="novareply">🧠 Nova: {nova}</div>', unsafe_allow_html=True)
    st.session_state.messages.append(("nova", nova))
    st.markdown(f'<script>typeText({repr(nova)}, "novareply");scrollToBottom();</script>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"💡 Mood: **{st.session_state.mood}**")
st.caption("💼 Developed by Solace + Nova 💫")

