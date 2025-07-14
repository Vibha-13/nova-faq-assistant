import streamlit as st
import spacy
import subprocess
import pandas as pd
import openai

# Load spaCy model with fallback
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Page settings
st.set_page_config(page_title="Nova FAQ Assistant", page_icon="🤖")
st.title("🤖 Nova - Your Smart FAQ Assistant")
st.write("Ask me any question based on your uploaded FAQ!")

# Upload FAQ file
uploaded_file = st.file_uploader("Upload your FAQ file (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("FAQ file uploaded successfully!")
    st.dataframe(df)

    # Ask a question
    user_question = st.text_input("Ask a question:")

    if user_question:
        # Combine all FAQ questions and answers into one text block
        faq_text = " ".join(df.astype(str).apply(lambda x: " ".join(x), axis=1))

        # Process user question and FAQ
        user_doc = nlp(user_question)
        faq_doc = nlp(faq_text)

        # Simple similarity (optional - this can be improved later)
        similarity_score = user_doc.similarity(faq_doc)

        st.write(f"🤔 Similarity Score: {similarity_score:.2f}")

        # Placeholder for response (real implementation may use OpenAI or vector DB)
        if similarity_score > 0.6:
            st.success("✅ I think I found something related!")
            # You could add a more detailed match or chunking logic here
        else:
            st.warning("⚠️ Sorry, I couldn't find anything relevant.")

else:
    st.info("📄 Please upload a CSV FAQ file to begin.")

