import streamlit as st
import pandas as pd
import spacy

# Try loading spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.error("spaCy model not found. Please ensure en_core_web_sm is properly installed.")
    st.stop()

st.set_page_config(page_title="Nova FAQ Assistant", page_icon="🤖")
st.title("🤖 Nova - Your Smart FAQ Assistant")
st.write("Ask me any question based on your uploaded FAQ!")

uploaded_file = st.file_uploader("Upload your FAQ file (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("FAQ file uploaded successfully!")
    st.dataframe(df)

    user_question = st.text_input("Ask a question:")

    if user_question:
        faq_text = " ".join(df.astype(str).apply(lambda x: " ".join(x), axis=1))
        user_doc = nlp(user_question)
        faq_doc = nlp(faq_text)
        similarity_score = user_doc.similarity(faq_doc)

        st.write(f"🤔 Similarity Score: {similarity_score:.2f}")

        if similarity_score > 0.6:
            st.success("✅ I think I found something related!")
        else:
            st.warning("⚠️ Sorry, I couldn't find anything relevant.")
else:
    st.info("📄 Please upload a CSV FAQ file to begin.")
