import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY") or st.secrets["openai"]["api_key"]

# Page config and branding
st.set_page_config(page_title="Nova – FAQ Assistant", page_icon="🤖", layout="centered")
st.sidebar.image("nova_bot.png", use_column_width=True)
st.sidebar.title("Nova – College FAQ Bot")
st.title("Nova – Ask your college FAQs 💬")

# Function to query OpenAI
def ask_nova(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Nova, a helpful assistant for college related queries."},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message["content"].strip()

# Text input section
user_input = st.text_input("Type your question here and hit Enter:")
if user_input:
    with st.spinner("Nova is thinking..."):
        answer = ask_nova(user_input)
    st.markdown("**Nova says:**")
    st.write(answer)
