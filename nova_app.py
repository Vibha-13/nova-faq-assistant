import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Nova FAQ Assistant", page_icon="🤖")
st.title("🤖 Nova - Your Smart FAQ Assistant")
st.write("Ask me any question based on your uploaded FAQ!")

uploaded_file = st.file_uploader("Upload your FAQ file (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("FAQ file uploaded successfully!")
    st.dataframe(df)

    if "Question" not in df.columns or "Answer" not in df.columns:
        st.error("CSV must have 'Question' and 'Answer' columns.")
        st.stop()

    user_question = st.text_input("Ask a question:")

    if user_question:
        # Vectorize user question and FAQ questions
        vectorizer = TfidfVectorizer().fit(df["Question"].astype(str))
        question_vectors = vectorizer.transform(df["Question"].astype(str))
        user_vector = vectorizer.transform([user_question])

        # Compute cosine similarity
        similarities = cosine_similarity(user_vector, question_vectors).flatten()
        best_match_idx = similarities.argmax()
        score = similarities[best_match_idx]

        st.write(f"🤔 Similarity Score: {score:.2f}")

        if score > 0.5:
            st.success("✅ Here's a relevant answer:")
            st.write(f"**Q:** {df['Question'][best_match_idx]}")
            st.write(f"**A:** {df['Answer'][best_match_idx]}")
        else:
            st.warning("⚠️ Sorry, I couldn't find anything relevant.")
else:
    st.info("📄 Please upload a CSV FAQ file to begin.")
