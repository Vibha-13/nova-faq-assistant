import streamlit as st
import openai
import toml
import os

# Load secrets from secrets.toml or Streamlit secrets
if os.path.exists("secrets.toml"):
    secrets = toml.load("secrets.toml")
    api_key = secrets["openrouter"]["api_key"]
    base_url = secrets["openrouter"]["base_url"]
else:
    api_key = st.secrets["openrouter"]["api_key"]
    base_url = st.secrets["openrouter"]["base_url"]

# Set OpenAI API credentials
openai.api_key = api_key
openai.base_url = base_url

# UI setup
st.set_page_config(page_title="Nova FAQ Assistant 🌟", page_icon="🤖", layout="centered")

with st.sidebar:
    st.title("🧠 Nova Assistant")
    st.markdown("Ask me anything about your project!")
    st.divider()
    st.markdown("⚙️ **Settings**")
    model = st.selectbox("Choose a model", ["openrouter/meta-llama-3-8b-instruct", "openrouter/google/gemma-7b-it"], index=0)

st.title("💬 Nova FAQ Assistant")
st.markdown("Ask your questions below:")

user_question = st.text_input("Enter your question below:")

if st.button("Ask Nova"):
    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are Nova, a friendly assistant who helps answer questions about projects clearly."},
                    {"role": "user", "content": user_question}
                ]
            )
            st.success("✅ Nova's Response:")
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ API Error: {e}")
