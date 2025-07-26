import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

if not openai.api_key:
    raise ValueError("❌ OPENROUTER_API_KEY not found. Please check your .env file.")

st.set_page_config(page_title="Nova FAQ Assistant", page_icon="✨")

st.markdown("## Nova FAQ Assistant 🌟")
st.markdown("Ask me anything about your project!")

with st.expander("⚙️ Settings"):
    model = st.selectbox("Choose a model", [
        "openrouter/mistral",
        "openrouter/cinematika",
        "openrouter/command-r"
    ])

question = st.text_input("Enter your question below:")

if st.button("Ask Nova"):
    if question:
        with st.spinner("Thinking..."):
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are Nova, a helpful assistant for project FAQs."},
                        {"role": "user", "content": question}
                    ]
                )
                answer = response['choices'][0]['message']['content']
                st.markdown(f"### 💬 Answer:\n{answer}")
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
