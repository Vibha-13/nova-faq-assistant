import streamlit as st
import openai
from PIL import Image

# Load and display logo in sidebar
st.sidebar.image("nova_bot.png", width=100)

# Title and UI
st.sidebar.markdown("## 🧠 Nova Assistant")
st.sidebar.markdown("Ask me anything about your project!")

st.sidebar.markdown("---")
st.sidebar.markdown("⚙️ **Settings**")
st.sidebar.markdown("Choose a model")

model = st.sidebar.selectbox(
    "Model",
    [
        "mistralai/mistral-7b-instruct",
        "meta-llama/llama-3-8b-instruct",
        "openai/gpt-3.5-turbo",
        "openai/gpt-4"
    ],
    index=1
)

# Set OpenRouter API config
openai.api_key = st.secrets["openrouter"]["api_key"]
openai.api_base = "https://openrouter.ai/api/v1"

st.title("💬 Nova FAQ Assistant")
st.markdown("Ask your questions below:")

user_question = st.text_input("Enter your question below:")

if st.button("Ask Nova") and user_question:
    try:
        with st.spinner("Nova is thinking..."):
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful project assistant."},
                    {"role": "user", "content": user_question}
                ]
            )
        st.success("✅ Nova's Response:")
        st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error("❌ API Error: " + str(e))
