import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Error if API key is missing
if not api_key:
    st.error("🔐 OPENAI_API_KEY not found in your .env file.")
    st.stop()

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Function to query Nova
def ask_nova(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are Nova ✨, a helpful FAQ assistant. Respond with friendly tone and use emojis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# --- Streamlit App Layout ---
st.set_page_config(page_title="Nova AI Assistant", page_icon="🤖", layout="wide")

# Sidebar with logo
with st.sidebar:
    st.image("nova_bot.png", width=160)
    st.markdown("## 💫 Nova – FAQ Bot")
    st.markdown("Ask me anything about your project!")
    st.markdown("---")
    st.markdown("Made with ❤️ by Solace")

# Main area
st.title("✨ Nova – Your AI FAQ Assistant")
st.markdown("Ask me your questions below and I’ll reply with a smile 😊")

# Multi-line user input
user_input = st.text_area("🔎 Your question:", placeholder="e.g., How to deploy the chatbot on GitHub Pages?", height=100)

# On submit
if user_input:
    with st.spinner("Nova is thinking... 💭"):
        try:
            response = ask_nova(user_input)
            st.success("✅ Nova says:")
            st.markdown(f"**{response}**")
        except Exception as e:
            st.error(f"⚠️ Oops! Error: {e}")
