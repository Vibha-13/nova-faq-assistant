import streamlit as st
import random
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

st.set_page_config(page_title="Nova FAQ Assistant", page_icon="🤖")

# ---------------------------------------------
# 🎨 Custom CSS for Styling
st.markdown("""
    <style>
        .stChatMessage {
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .stTextInput > div > input {
            background-color: #ffffff;
            border: 1px solid #ccc;
        }
        .block-container {
            padding-top: 2rem;
        }
        span.dots::after {
            content: '...';
            animation: blink 1s infinite;
        }
        @keyframes blink {
            0%, 100% { opacity: 0; }
            50% { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------
# 🌟 Sidebar with Nova Logo + Greeting
st.sidebar.image("nova_bot.png", use_container_width=True)
st.sidebar.markdown("👋 **Hello! I'm Nova**\n\nAsk me anything related to your project, and I’ll help you out!")

# 💡 Random Tip of the Day
tips = [
    "Keep your README.md updated – it's your project’s CV!",
    "Document your functions with clear comments 💬",
    "Push code often – Git is your friend! 💾",
    "Break down big problems into small tasks 🧩",
    "Don't forget to test your app regularly! 🧪"
]
st.sidebar.markdown(f"💡 **Tip of the Day:**\n> {random.choice(tips)}")

# 🧹 Clear Chat Option
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = [{"role": "system", "content": "You are Nova, a helpful assistant for answering FAQ about the project."}]
    st.experimental_rerun()

# ---------------------------------------------
# 🧠 Chat Message Memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Nova, a helpful assistant for answering FAQ about the project."}
    ]

# 💬 Display past messages
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------
# 🎤 Chat Input
if prompt := st.chat_input("Ask your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ⏳ Typing animation
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤖 Nova is typing<span class='dots'>.</span>", unsafe_allow_html=True)

        # Call OpenAI API
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages,
                temperature=0.6,
            )
            assistant_reply = response.choices[0].message.content
        except Exception as e:
            assistant_reply = f"⚠️ Something went wrong: {e}"

        message_placeholder.markdown(assistant_reply)
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
