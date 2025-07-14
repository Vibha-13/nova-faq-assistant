import streamlit as st
import pandas as pd
import spacy

st.set_page_config(page_title="Nova FAQ Assistant", page_icon="💬")

@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")

nlp = load_model()

def load_faq_data():
    df = pd.read_csv("faq_data.csv")
    return df

def get_best_answer(question, df):
    doc1 = nlp(question)
    best_score = 0
    best_answer = "❌ Sorry, I couldn't find a matching answer. Try rephrasing it!"

    for _, row in df.iterrows():
        doc2 = nlp(row["question"])
        score = doc1.similarity(doc2)
        if score > best_score:
            best_score = score
            best_answer = row["answer"]
    return best_answer

st.title("💬 Nova FAQ Assistant")
st.write("Ask me a question from your FAQ dataset:")

faq_data = load_faq_data()

user_question = st.text_input("🔍 Enter your question here:")

if user_question:
    answer = get_best_answer(user_question, faq_data)
    st.success(answer)
