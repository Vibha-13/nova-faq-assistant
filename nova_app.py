import streamlit as st
import requests

# --- Optional: Load from st.secrets (recommended for deployment) ---
API_KEY = st.secrets.get("openrouter", {}).get("api_key", "")
BASE_URL = st.secrets.get("openrouter", {}).get("base_url", "https://openrouter.ai/api/v1/chat")

# --- If you want to test locally without st.secrets, uncomment below ---
# API_KEY = "your-openrouter-key-here"
# BASE_URL = "https://openrouter.ai/api/v1/chat"

# --- App UI ---
st.set_page_config(page_title="Nova FAQ Assistant", page_icon="🧠")

st.sidebar.title("🧠 Nova Assistant")
st.sidebar.write("Ask me anything about your project!")

# Show logo if exists
try:
    with open("nova_bot.png", "rb") as img_file:
        st.sidebar.image(img_file, width=150)
except FileNotFoundError:
    st.sidebar.write("🖼️ Nova bot image not found.")

st.sidebar.markdown("### ⚙️ Settings")
model = st.sidebar.selectbox("Choose a model", [
    "openrouter/meta-llama-3-8b-instruct",
    "openrouter/mistral-7b-instruct",
    "openrouter/gpt-3.5-turbo",
])

st.title("💬 Nova FAQ Assistant")
st.markdown("Ask your questions below:")

user_input = st.text_area("Enter your question below:")

if st.button("Submit"):
    if not user_input.strip():
        st.warning("Please enter a question.")
    elif not API_KEY:
        st.error("API key not set. Check secrets or hardcoded key.")
    else:
        with st.spinner("Thinking..."):
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are Nova, a helpful assistant for answering project-related queries."},
                    {"role": "user", "content": user_input}
                ]
            }
            try:
                response = requests.post(BASE_URL, headers=headers, json=payload)
                response.raise_for_status()
                result = response.json()
                reply = result['choices'][0]['message']['content']
                st.success("✅ Nova's Response:")
                st.markdown(reply)
            except Exception as e:
                st.error(f"❌ API Error: {e}")
