import streamlit as st
import subprocess
import sys
import importlib
import pandas as pd

# --- Install missing packages at runtime ---
def install_if_needed(package, pip_name=None):
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", pip_name or package
        ])

install_if_needed("spacy")
install_if_needed("en_core_web_sm", "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl")

# --- Load spaCy model ---
import spacy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# --- Streamlit UI ---
st.set_page_config(page_title="Nova FAQ Assistant", page_icon="🤖")
st.title("🤖 Nova - Your Smart FAQ Assistant")
st.write("Ask me any question based on your uploaded FAQ!")

# --- Upload FAQ CSV file ---
uploaded_file = st.file_uploader("Upload your FAQ file (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ FAQ file uploaded successfully!")
    st.dataframe(df)

    # --- User asks a question ---
    user_question = st.text_input("Ask a question:")

    if user_question:
        # Combine all rows (questions + answers) into one block of text
        faq_text = " ".join(df.astype(str).apply(lambda row: " ".join(row), axis=1))

        user_doc = nlp(user_question)
        faq_doc = nlp(faq_text)

        similarity = user_doc.similarity(faq_doc)

        st.write(f"🔍 Similarity Score: {similarity:.2f}")

        if similarity > 0.6:
            st.success("✅ I think I found something related!")
        else:
            st.warning("⚠️ Sorry, I couldn't find anything relevant.")
else:
    st.info("📄 Please upload a CSV FAQ file to begin.")
