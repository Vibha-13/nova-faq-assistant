import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from difflib import SequenceMatcher

# 🎯 Together AI Setup
api_key = st.secrets["together"]["api_key"]
client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# 🎨 Page Config
st.set_page_config(page_title="Nova - Smart FAQ Assistant", page_icon="🤖")

# 📸 Sidebar UI
with st.sidebar:
    if os.path.exists("nova_bot.png"):
        st.image("nova_bot.png", caption="Nova, your smart assistant 🤖", use_container_width=True)
    else:
        st.warning("⚠️ 'nova_bot.png' not found in the app folder.")
    
    st.markdown("### Built by **Solace** & **Nyx** ✨")
    st.markdown("---")
    st.markdown("💬 Ask me anything from your FAQ!")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []

# 📁 Load FAQ Data
FAQ_FILE = "faqs.csv"

@st.cache_data
def load_faq():
    return pd.read_csv(FAQ_FILE)

if not os.path.exists(FAQ_FILE):
    st.error("🚨 'faqs.csv' not found. Add it and reload.")
    st.stop()

df = load_faq()
faq_qa = list(zip(df["Question"].astype(str), df["Answer"].astype(str)))

# 💬 Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Nova - Smart FAQ Assistant")
st.markdown("Nova loads your FAQ and chats with you smartly. If she can’t find an answer, she’ll ask GPT 📡")

# 📝 Chat Input
user_input = st.chat_input("Ask your question...")

# 🧠 Similarity function
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# 🔁 Process Input
if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Step 1: Try matching from FAQ
    best_match = None
    best_score = 0.0
    for q, a in faq_qa:
        score = similarity(user_input, q)
        if score > best_score:
            best_score = score
            best_match = (q, a)
    
    if best_score > 0.6:
        reply = best_match[1]
    else:
        # Step 2: GPT Fallback
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are Nova, a helpful and warm AI assistant trained on FAQ data."}
                ] + st.session_state.messages
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"⚠️ GPT failed: {e}"

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})

# 💬 Display Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
