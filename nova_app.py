import streamlit as st
import pandas as pd
import spacy
import random
from datetime import datetime

# Load spaCy NLP model
nlp = spacy.load("en_core_web_md")

# Load FAQ data
faq_data = pd.read_csv("faqs.csv")

# ------------------ Streamlit UI Setup ------------------

st.set_page_config(page_title="NOVA – Smart FAQ Assistant", page_icon="🌌")

# Custom CSS
st.markdown(
    """
    <style>
        .main { background-color: #0f1117; color: white; }
        .stTextInput > div > div > input {
            background-color: #1e2130;
            color: white;
        }
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.title("🌌 NOVA")
    st.markdown("Your Personal Tech FAQ Assistant 🤖")
    st.markdown("---")
    st.markdown("Built with ❤️ using Python + spaCy + Streamlit")
    st.markdown("By **Solace** ✨")
    st.markdown("---")
    st.caption("💡 Try asking: *'Start AI?'*, *'TCP vs UDP'* or *'Lost in tech'*")

# Title
st.markdown("<h2 style='color:#FFD700;'>Ask NOVA 💬</h2>", unsafe_allow_html=True)

# User input
user_question = st.text_input("👤 You:")

# ✨ Motivational quotes
quotes = [
    "🌟 Keep going, your future self will thank you.",
    "🚀 One small step every day builds greatness.",
    "🧠 Learning never exhausts the mind.",
    "✨ Even tech queens start somewhere.",
    "📈 You’re not behind — you’re just building differently."
]

# Answer logic
if user_question:
    user_doc = nlp(user_question)
    best_score = 0
    best_answer = "🤖 I'm still learning. I don’t have an answer for that yet."

    for _, row in faq_data.iterrows():
        faq_doc = nlp(row["Question"])
        score = user_doc.similarity(faq_doc)
        if score > best_score:
            best_score = score
            best_answer = row["Answer"]

    # Display NOVA's answer
    st.markdown(f"""
        <div style='
            padding: 1em;
            background-color: #2a2d40;
            border-radius: 10px;
            color: #FFD700;
            font-size: 16px;
        '>
            <strong>🪄 NOVA:</strong> {best_answer}
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='margin-top: 2em; color: #999;'>{random.choice(quotes)}</div>", unsafe_allow_html=True)

    # Feedback buttons
    st.write("**Was this helpful?**")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("👍 Yes"):
            feedback = {
                "timestamp": datetime.now(),
                "question": user_question,
                "answer": best_answer,
                "feedback": "👍"
            }
            df = pd.DataFrame([feedback])
            df.to_csv("feedback_log.csv", mode="a", header=not pd.io.common.file_exists("feedback_log.csv"), index=False)
            st.success("Thanks for your feedback! 💖")
    with col2:
        if st.button("👎 No"):
            feedback = {
                "timestamp": datetime.now(),
                "question": user_question,
                "answer": best_answer,
                "feedback": "👎"
            }
            df = pd.DataFrame([feedback])
            df.to_csv("feedback_log.csv", mode="a", header=not pd.io.common.file_exists("feedback_log.csv"), index=False)
            st.info("Feedback noted. NOVA will try to improve 💡")
