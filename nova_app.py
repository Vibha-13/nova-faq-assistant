# nova_app.py

import streamlit as st
import openai
import os

# ------------------ SETTINGS ------------------

st.set_page_config(page_title="🧠 Nova - Your FAQ Assistant", layout="centered")

# Replace with your OpenAI API key (or use .env and os.environ if you want it safe)
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# ------------------ SIDEBAR ------------------

st.sidebar.title("🧠 Nova Settings")
mood = st.sidebar.selectbox("Choose Nova’s Mood", ["Friendly", "Sassy", "Professional", "Chill", "Funny"])
clear_chat = st.sidebar.button("🗑️ Clear Conversation")

# ------------------ FUNCTION ------------------

def generate_nova_response(user_input, mood):
    mood_prefix = {
        "Friendly": "Answer in a warm and friendly tone.",
        "Sassy": "Answer with playful sass and confidence, like a Gen Z diva.",
        "Professional": "Answer in a formal, informative tone.",
        "Chill": "Keep it super chill and laid-back like a cool bestie.",
        "Funny": "Make the reply humorous and quirky with emojis or jokes."
    }

    prompt = f"""
You are Nova, an AI FAQ assistant. Your job is to answer user questions about any topic (especially tech, college, AI, etc).
{mood_prefix[mood]}

User: {user_input}
Nova:"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=200
    )

    return response['choices'][0]['message']['content'].strip()

# ------------------ MAIN UI ------------------

st.markdown("### 🧠 Nova - Your FAQ Assistant")
st.markdown("_Ask me anything about your project. Nova’s got brains and personality 😎_")

if "messages" not in st.session_state or clear_chat:
    st.session_state.messages = []

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 Ask your question:")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.messages.append(("You", user_input))
    with st.spinner("Nova is typing..."):
        reply = generate_nova_response(user_input, mood)
        st.session_state.messages.append(("Nova", reply))

# ------------------ CHAT DISPLAY ------------------

for sender, msg in st.session_state.messages:
    if sender == "You":
        st.markdown(f"**👤 You:** {msg}")
    else:
        st.markdown(f"**🧠 Nova:** {msg}")
