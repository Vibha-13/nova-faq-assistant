import streamlit as st
import pandas as pd
import openai

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Nova - FAQ Assistant", page_icon="🤖")
st.title("🤖 Nova - Your Smart FAQ Assistant")
st.write("Ask me anything related to your uploaded FAQ!")

uploaded_file = st.file_uploader("Upload your FAQ CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ FAQ uploaded successfully!")
    st.dataframe(df)

    question = st.text_input("💬 Ask your question:")

    if question:
        with st.spinner("Thinking..."):
            context = ""
            for i, row in df.iterrows():
                context += f"Q: {row['Question']}\nA: {row['Answer']}\n\n"

            prompt = f"""You are Nova, an intelligent FAQ assistant.
Use the following FAQ to answer the user's question:

{context}

User's Question: {question}
Answer:"""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            answer = response['choices'][0]['message']['content'].strip()
            st.success("🧠 Nova says:")
            st.write(answer)
else:
    st.info("📄 Please upload the FAQ CSV file to begin.")
