import streamlit as st
import requests

st.set_page_config(page_title="Nova Assistant", page_icon="🧠", layout="centered")

# Sidebar
st.sidebar.title("🧠 Nova FAQ Assistant")
st.sidebar.markdown("""
**🗂️ Project**: Interactive AI FAQ Assistant  
**🧪 Model**: Choose any from OpenRouter  
**📌 Instructions**:  
1. Enter your OpenRouter API key in `.streamlit/secrets.toml`  
2. Select your desired model  
3. Type your question & hit enter  
""")

# Optional logo
try:
    st.sidebar.image("nova_bot.png", width=150)
except:
    st.sidebar.caption("🤖")

# API key
api_key = st.secrets.get("openrouter", {}).get("api_key")

if not api_key:
    st.error("⚠️ Please add your OpenRouter API key to `.streamlit/secrets.toml` like this:\n\n```toml\n[openrouter]\napi_key = \"your-key-here\"\n```")
    st.stop()

# Model select
model = st.sidebar.selectbox("⚙️ Choose a model", [
    "openrouter/mistral",
    "openrouter/meta-llama-3-8b-instruct",
    "openrouter/openchat-3.5-1210",
    "openrouter/cinematika-7b",
    "openrouter/gpt-3.5-turbo",  # If you have it
], index=0)

# System prompt
system_prompt = "You are Nova, a helpful AI assistant designed to answer project FAQs and guide users in a friendly, concise, and engaging way."

# Input box
st.title("Nova - AI FAQ Assistant 💬")
user_question = st.text_input("Enter your question below:")

if user_question:
    with st.spinner("Nova is typing..."):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "streamlit-nova-assistant",  # customize if you want
                    "X-Title": "Nova FAQ Assistant",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_question}
                    ]
                },
                timeout=30
            )

            if response.status_code == 200:
                output = response.json()
                reply = output["choices"][0]["message"]["content"]
                st.success("✅ Nova's Response:")
                st.markdown(reply)
            else:
                st.error(f"❌ API Error {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"⚠️ Exception: {e}")
