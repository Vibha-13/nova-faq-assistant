import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Get API Key
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("❌ OPENROUTER_API_KEY not found. Please check your .env file.")

# Initialize client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# Sidebar with emoji and logo
st.sidebar.image("nova_bot.png", width=150)
st.sidebar.markdown("## 🤖 Nova FAQ Assistant")
st.sidebar.markdown("**Ask me anything about your project!**")
st.sidebar.markdown("---")
st.sidebar.markdown("🌐 Powered by [OpenRouter](https://openrouter.ai)")

# Main UI
st.title("💬 Ask Nova – Your AI FAQ Assistant")
user_input = st.text_input("What do you want to know?", "")

if st.button("Submit") or user_input:
    with st.spinner("Nova is thinking..."):
        try:
            response = client.chat.completions.create(
                model="mistralai/mixtral-8x7b",
                messages=[
                    {"role": "system", "content": "You're a helpful assistant for student project FAQs."},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response.choices[0].message.content
            st.success("Here's what I found:")
            st.write("🧠", answer)
        except Exception as e:
            st.error(f"🚨 Error: {str(e)}")
