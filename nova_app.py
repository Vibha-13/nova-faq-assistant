import streamlit as st
import pandas as pd
import spacy
import subprocess
import openai
import random
from datetime import datetime

# Automatically install the spaCy model if missing
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    st.warning("Downloading spaCy model... please wait ⏳")
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_md"])
    nlp = spacy.load("en_core_web_md")

# Load FAQ data
def load_faqs():
    return pd.DataFrame({
        "question": [
            "What is a microcontroller?",
            "Applications of microcontrollers?",
            "What is an embedded system?",
            "Difference between microprocessor and microcontroller?",
            "What languages are used in microcontroller programming?",
            "What is Flash memory in microcontrollers?"
        ],
        "answer": [
            "A microcontroller is an integrated circuit designed to perform specific operations in embedded systems.",
            "Microcontrollers are used in washing machines, automobiles, medical devices, and IoT gadgets.",
            "An embedded system is a computer system with a dedicated function within a larger system.",
            "A microcontroller has CPU, RAM, ROM and peripherals on a single chip, while a microprocessor has only the CPU.",
            "Microcontrollers are typically programmed in C, C++, or assembly language.",
            "Flash memory is non-volatile storage used to store the program code of a microcontroller."
        ]
    })

# Semantic similarity using spaCy
def get_best_answer(user_question, faqs):
    user_doc = nlp(user_question)
    scores = []
    for i, q in enumerate(faqs['question']):
        score = user_doc.similarity(nlp(q))
        scores.append((score, i))
    best_score, best_index = max(scores)
    if best_score > 0.75:
        return faqs['answer'][best_index]
    else:
        return None

# GPT fallback if no good FAQ match
def get_gpt_answer(user_question):
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": user_question
        }]
    )
    return response.choices[0].message.content.strip()

# UI setup
st.set_page_config(page_title="NOVA: FAQ + AI Assistant", page_icon="🤖")
st.title("✨ NOVA - Your Project FAQ Assistant")

# Sidebar
with st.sidebar:
    st.image("https://i.imgur.com/H3JbG1r.png", width=150)
    st.markdown("Ask me anything about your project!")
    st.markdown("Created with ❤️ by Solace & Nyx")

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask a question...")

if user_input:
    faqs = load_faqs()
    with st.chat_message("user"):
        st.markdown(user_input)

    # Try answering from FAQs
    answer = get_best_answer(user_input, faqs)

    if answer is None:
        answer = get_gpt_answer(user_input)

    with st.chat_message("ai"):
        st.markdown(answer)
    st.session_state.messages.append((user_input, answer))

# Display chat history
for user_msg, bot_reply in st.session_state.messages:
    st.chat_message("user").markdown(user_msg)
    st.chat_message("ai").markdown(bot_reply)

# Footer with fun message
st.markdown("---")
st.caption(f"🧠 NOVA is running on {datetime.now().strftime('%A, %d %B %Y')}. Stay curious!")
