import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# --- Load environment variables ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found. Please check your .env file.")

# --- Initialize OpenAI client ---
client = OpenAI(api_key=api_key)

# --- Streamlit UI ---
st.set_page_config(page_title="Nova: FAQ Assistant", page_icon="🤖")
st.sidebar.image("nova_bot.png", width=150)
st.sidebar.title("🌟 Nova Assistant")
st.sidebar.markdown("Ask your FAQs, get instant answers!")

st.title("💬 Nova: Your FAQ Assistant")
st.markdown("Type a question below and let Nova help you!")

# --- Session storage ---
if "chat" not in st.session_state:
    st.session_state.chat = []

# --- Input form ---
with st.form("user_input"):
    user_query = st.text_input("Ask Nova something:")
    submitted = st.form_submit_button("Ask 🔍")

if submitted and user_query:
    st.session_state.chat.append(("You", user_query))

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Nova, a helpful assistant."},
                {"role": "user", "content": user_query},
            ]
        )
        reply = response.choices[0].message.content.strip()
        st.session_state.chat.append(("Nova 🤖", reply))
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

# --- Display chat history ---
for sender, msg in st.session_state.chat:
    if sender == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Nova:** {msg}")
