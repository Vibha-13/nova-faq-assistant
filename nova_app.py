import streamlit as st
import requests

st.set_page_config(page_title="Nova AI Assistant", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.image("nova_bot.png", width=100, caption="Nova ☄️")
    st.title("Nova AI Assistant")
    st.markdown("Talk to a smart bot powered by **OpenRouter** + ChatGPT & more 🤖")

    model_choice = st.selectbox(
        "Choose a model",
        options=["gpt-3.5-turbo", "gpt-4", "mistral", "llama3-8b", "gemma-7b-it"],
        index=0,
    )

    dark_mode = st.toggle("🌙 Dark Mode")
    if dark_mode:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0e1117;
            color: #FAFAFA;
        }
        .stMarkdown, .stChatMessage {
            color: #FAFAFA !important;
        }
        .stChatMessage .markdown-text-container {
            color: #FAFAFA !important;
        }
        .stTextInput > div > input {
            background-color: #2c2f35;
            color: #FAFAFA;
        }
        .stButton>button {
            background-color: #1f1f1f;
            color: #FAFAFA;
            border: 1px solid #888;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    if st.button("🧼 Clear Chat"):
        st.session_state.messages = []
        st.session_state.count = 0
       st.rerun()

# --- Session State Init ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "count" not in st.session_state:
    st.session_state.count = 0

# --- Title ---
st.title("💬 Nova Chatbot")
st.markdown("Ask anything, and Nova will help you out!")

# --- Prompt Templates ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📝 Summarize"):
        st.session_state.prompt = "Can you summarize this?"
with col2:
    if st.button("✍️ Rephrase"):
        st.session_state.prompt = "Please rephrase this in a better way:"
with col3:
    if st.button("🧹 Fix Grammar"):
        st.session_state.prompt = "Correct the grammar in this sentence:"

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Input ---
user_input = st.chat_input("Type your message here...")

if user_input or "prompt" in st.session_state:
    content = st.session_state.get("prompt", "") + "\n" + (user_input or "")
    st.session_state.messages.append({"role": "user", "content": content})
    with st.chat_message("user"):
        st.markdown(content)

    # Reset prompt
    st.session_state.pop("prompt", None)

    # --- Spinner while waiting ---
    with st.spinner("Nova is thinking..."):
        try:
            api_key = st.secrets["OPENROUTER_API_KEY"]
            headers = {
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://yourdomain.com",
                "X-Title": "NovaAI-Chat",
            }

            payload = {
                "model": model_choice,
                "messages": st.session_state.messages,
                "stream": False,
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30,
            )

            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"]
            else:
                reply = f"⚠️ Error {response.status_code}: {response.text}"

        except Exception as e:
            reply = f"🚨 Failed to fetch response: {str(e)}"

    # --- Display AI Reply ---
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.count += 1

# --- Stats Footer ---
st.markdown("---")
st.markdown(f"🧠 Messages exchanged: **{st.session_state.count}**")
st.caption("Built with ❤️ by Solace + Nyx ⚡️ | Powered by OpenRouter APIs")

