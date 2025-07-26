import streamlit as st
from openai import OpenAI
import os

# Set OpenRouter endpoint
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)

# Set Streamlit page config
st.set_page_config(
    page_title="🧠 Nova FAQ Assistant",
    layout="centered",
    page_icon="🧠"
)

# Sidebar with branding image
st.sidebar.image("nova_bot.png", use_column_width=True)
st.sidebar.title("🧠 Nova Assistant")
st.sidebar.markdown("Ask me anything about your project!")

# Chat input area
st.title("💬 Nova FAQ Assistant")
st.markdown("Ask your questions below:")

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are Nova, a smart and friendly FAQ assistant for student projects. Answer clearly and helpfully."
        }
    ]

# Show chat history
for msg in st.session_state.messages[1:]:  # skip system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
prompt = st.chat_input("Enter your question below:")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Show thinking message
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ Nova is thinking...")

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",
            messages=st.session_state.messages,
            stream=True,
        )

        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })

    except Exception as e:
        message_placeholder.markdown(f"❌ API Error:\n\n{e}")
