# nova_app.py

import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
from PIL import Image

# --- Load environment variables --- #
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found. Please check your .env file.")

# --- Initialize OpenAI client --- #
client = OpenAI(api_key=api_key)

# --- Sidebar --- #
st.sidebar.image("nova_bot.png", use_column_width=True)
st.sidebar.title("Nova FAQ Assistant 🤖")
st.sidebar.markdown("Your AI-powered college buddy to answer all your doubts!")

# --- Page Setup --- #
st.set_page_config(page_title="Nova FAQ Assistant", page_icon="🧠")
st.title("📚 Ask Nova Anything!")
st.markdown("Type your question below and Nova will try its best to help 💡")

# --- Input Area --- #
question = st.text_input("📝 Your Question:", placeholder="E.g., How do I register for an elective?")

# --- Emoji Categories --- #
st.markdown("### 🔍 Topics you can try:")
cols = st.columns(5)
with cols[0]: st.button("📅 Time Table")
with cols[1]: st.button("🧾 Exams")
with cols[2]: st.button("🏫 Courses")
with cols[3]: st.button("📨 Contact")
with cols[4]: st.button("📚 Resources")

# --- Process the Input --- #
if question:
    with st.spinner("Nova is thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Nova, a helpful and friendly assistant for answering college-related FAQs."},
                    {"role": "user", "content": question}
                ]
            )
            answer = response.choices[0].message.content
            st.success("✅ Nova's Answer:")
            st.markdown(f"{answer}")
        except Exception as e:
            st.error("❌ Something went wrong. Please try again.")
            st.exception(e)

# --- Footer --- #
st.markdown("---")
st.markdown("Made with ❤️ by Solace & Nyx")
