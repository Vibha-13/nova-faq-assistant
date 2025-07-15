import streamlit as st
import pandas as pd
import spacy

# Load spaCy model safely
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.error("spaCy model not found. Please make sure 'en_core_web_sm' is installed.")
    st.stop()

# Page config
st.set_page_config(page_title="Nova FAQ Assistant", page_icon="🤖")
st.title("🤖 Nova - Your Smart FAQ Assistant")
st.write("Ask me any question based on your uploaded or default FAQ!")

# Load default FAQ
DEFAULT_FAQ_FILE = "faq.csv"

# Try loading default file
df = None
default_loaded = False
try:
    df = pd.read_csv(DEFAULT_FAQ_FILE)
    default_loaded = True
    st.success("Default FAQ file loaded successfully.")
except FileNotFoundError:
    st.info("No default FAQ file found. Please upload one.")

# File uploader for optional upload
uploaded_file = st.file_uploader("📄 Upload a new FAQ file (CSV) to replace default", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Uploaded FAQ file loaded successfully.")
    default_loaded = False

# If we have a dataframe to work with
if df is not None:
    st.dataframe(df)

    user_question = st.text_input("🧠 Ask a question:")

    if user_question:
        # Combine all FAQ rows into one string block
        faq_text = " ".join(df.astype(str).apply(lambda row: " ".join(row), axis=1))

        user_doc = nlp(user_question)
        faq_doc = nlp(faq_text)
        similarity_score = user_doc.similarity(faq_doc)

        st.write(f"🤔 Similarity Score: `{similarity_score:.2f}`")

        if similarity_score > 0.6:
            st.success("✅ I think I found something related!")
        else:
            st.warning("⚠️ Sorry, I couldn't find anything relevant.")
else:
    st.info("⚠️ Please upload a CSV FAQ file to begin.")
