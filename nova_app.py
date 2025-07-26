import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenRouter API Key
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("❌ OPENROUTER_API_KEY not found. Please check your .env file.")

# Streamlit UI
st.set_page_config(page_title="Nova FAQ Assistant 🤖", layout="centered")
st.title("Nova FAQ Assistant 🌟")
st.markdown("Ask me anything about your project!")

# Sidebar Image (optional)
st.sidebar.image("nova_bot.png", use_column_width=True)
st.sidebar.markdown("Built with 💙 by Solace")

# User Input
question = st.text_input("Enter your question below:")

# Model and endpoint
model = "mistral/mistral-7b-instruct"  # ✅ valid OpenRouter model
api_url = "https://openrouter.ai/api/v1/chat/completions"

# Function to ask OpenRouter
def get_answer(question):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are Nova, a helpful FAQ assistant for AI/ML networking projects."},
            {"role": "user", "content": question}
        ]
    }

    response = requests.post(api_url, headers=headers, json=body)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        st.error(f"⚠️ Error: {response.status_code} - {response.json()}")
        return None

# Process user question
if question:
    with st.spinner("Nova is thinking... 🧠"):
        answer = get_answer(question)
        if answer:
            st.markdown("### Nova says:")
            st.write(answer)
