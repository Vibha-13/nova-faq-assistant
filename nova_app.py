import streamlit as st
import spacy
import openai
import pandas as pd

st.set_page_config(page_title="Nova: FAQ Assistant", page_icon="💬")

# Title
st.title("💬 Nova - FAQ Assistant")

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.error("spaCy model 'en_core_web_sm' is not installed. Please make sure it's listed in requirements.txt.")
    st.stop()

# Set your OpenAI key securely (use Streamlit secrets in production)
openai.api_key = st.secrets.get("OPENAI_API_KEY", "sk-...")  # fallback for local use

# Load sample FAQ dataset (replace with your own or upload option)
@st.cache_data
def load_faqs():
    data = {
        "question": [
            "What are your working hours?",
            "How can I reset my password?",
            "Where is your office located?",
            "Do you offer refunds?",
            "How can I contact support?"
        ],
        "answer": [
            "Our working hours are Monday to Friday, 9am to 5pm.",
            "To reset your password, click on 'Forgot Password' on the login page.",
            "Our office is located at 123 Tech Park, Silicon Valley.",
            "Yes, we offer refunds within 30 days of purchase.",
            "You can contact support via email at support@example.com."
        ]
    }
    return pd.DataFrame(data)

faq_df = load_faqs()

# Function to find most similar question using spaCy
def find_best_match(user_question):
    user_doc = nlp(user_question)
    similarities = faq_df["question"].apply(lambda x: nlp(x).similarity(user_doc))
    best_match_idx = similarities.idxmax()
    return faq_df.iloc[best_match_idx]["answer"], similarities[best_match_idx]

# User input
user_query = st.text_input("Ask a question ❓", placeholder="E.g., How do I reset my password?")

if user_query:
    with st.spinner("Thinking..."):
        answer, score = find_best_match(user_query)
        if score < 0.65:
            st.warning("🤔 I'm not very confident in the match, but here's a possible answer:")
        st.success(answer)

    st.markdown("---")
    st.markdown(f"**Similarity Score:** `{score:.2f}` (Debug Info)")

