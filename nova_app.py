import streamlit as st
import pandas as pd
import spacy
import random
import subprocess
from datetime import datetime

# Load spaCy model (auto-download if not found)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.warning("⏳ Downloading spaCy model... please wait a moment.")
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Load FAQ data
def load_faq_data():
    df = pd.read_csv("faq_data.csv")  # Replace with your actual file if different
    return df

# Get most relevant answer using spaCy similarity
def get_best_answer(question, df):
    doc1 = nlp(question)
    max_score = 0
    best_answer = "Sorry, I couldn't find an answer. Try rephrasing."

    for i, row in df.iterrows():
        doc2 = nlp(row["question"])
        similarity = doc1.similarity(doc2)
        if similarity > max_score:
            max_score = similarity
            best_answer = row["answer"]
    return best_answer

# Streamlit App
st.set_page_config(page_title="Nova FAQ Assistant", page_icon="💬")

st.title("💬 Nova FAQ Assistant")
st.markdown("Ask me anything about the project!")

faq_data = load_faq_data()

question_input = st.text_input("❓ Type your question here")

if question_input:
    answer = get_best_answer(question_input, faq_data)
    st.success(answer)

    # Bonus feature: fun emoji feedback
    if "thanks" in question_input.lower():
        st.balloons()
