import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variable
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Page configuration
st.set_page_config(page_title="Nova FAQ Assistant 💡", page_icon="🤖", layout="wide")

# Sidebar styling
with st.sidebar:
    st.title("✨ Nova FAQ Assistant")
    st.markdown("Ask me anything from your FAQ sheet 💬")
    st.markdown("💡 AI powered by OpenAI")
    st.markdown("---")
    st.markdown("Made with ❤️ by Solace")

# Chat header
st.markdown("<h1 style='text-align: center;'>🤖 Nova Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ask Nova your doubts, and it'll reply with magic! ✨</p>", unsafe_allow_html=True)

# Chat history state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask your question here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get assistant reply
    with st.chat_message("assistant"):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Nova, a friendly assistant designed to help users with FAQ-style queries. Respond clearly and politely."},
                    *st.session_state.messages,
                ],
                temperature=0.6
            )
            assistant_reply = response.choices[0].message["content"]
        except Exception as e:
            assistant_reply = "⚠️ Nova couldn't reach OpenAI servers. Try again later."

        st.markdown(assistant_reply)
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
