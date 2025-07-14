import streamlit as st
import spacy
import subprocess
import openai
import pandas as pd

# Load spaCy model safely
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.warning("Downloading spaCy model... please wait ⏳")
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# App content below
st.title("Nova FAQ Assistant 🤖")
st.write("Ask me something!")

user_input = st.text_input("Your question")

if user_input:
    doc = nlp(user_input)
    st.write("Tokens:", [token.text for token in doc])
    st.success("Processed input using spaCy.")
