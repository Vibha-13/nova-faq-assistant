import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from difflib import SequenceMatcher

# 🎯 API Setup (Together API)
api_key = st.secrets["together"]["api_key"]
client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")

MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# 📁 Auto-load FAQ from local file
FAQ_FILE = "faqs.csv"
if not os.path.exists(FAQ_FILE):
    st.error("🚨 FAQ file not found! Please ensure 'faqs.csv' is in the app folder.")
    st.stop()

# 📚 Load FAQ data
df = pd.read_csv(FAQ_FILE)
faq_qa = list(zip(df["Question"].astype(str), df["Answer"].astype(str)))

# 🎨 Streamlit page config
st.set_page_config(page_title="Nova - Smart FAQ Assistant", page_icon="🤖")

# 📸 Sidebar
with st.sidebar:
    try:
        st.image("nova_bot.png", caption="Nova, your smart assistant 🤖", use_container_width=True)
    except Exception as e:
        st.warning("⚠️ Could not load image. Make sure 'nova_bot.png' is in the app folder.")
    st.markdown("### Built by **Solace** & **Nyx** ✨")
    st.markdown("---")
    st.markdown("💡 Nova reads your FAQ and finds the best answer.\nIf unsure, she asks GPT for help!")

# 🧠 Main UI
st.title("🤖 Nova - Smart FAQ Assistant")
st.markdown("#### Ask anything from the loaded FAQ file 📄")
st.markdown("🧠 Nova auto-loads your FAQ! Just type your question 👇")

# 📝 Input
user_question = st.text_input("💬 Ask your question:")

# 🔍 Process input
if user_question:
    def similarity(a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    best_match = None
    best_score = 0.0
    for q, a in faq_qa:
        score = similarity(user_question, q)
        if score > best_score:
            best_score = score
            best_match = (q, a)

    if best_score > 0.6:
        st.success(f"✅ Found a relevant FAQ (Similarity: {best_score:.2f})")
        st.markdown(f"**Q:** {best_match[0]}")
        st.markdown(f"**🧠 Nova says:** {best_match[1]}")
    else:
        st.warning("🤔 Couldn't find an exact match, asking GPT instead...")
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are Nova, a helpful AI FAQ assistant who answers clearly and encouragingly."},
                    {"role": "user", "content": user_question}
                ]
            )
            answer = response.choices[0].message.content.strip()
            st.markdown("**🤖 Nova says:**")
            st.info(answer)
        except Exception as e:
            st.error("❌ GPT failed to respond. Here's the full error:")
            st.exception(e)
