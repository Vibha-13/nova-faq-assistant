import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Set up OpenAI client
client = OpenAI(api_key=api_key)

# Define assistant prompt
assistant_prompt = """
You are Nova, a helpful virtual assistant built to answer questions related to college FAQs, rules, facilities, placement procedures, and general academic queries.
Always answer concisely, helpfully, and in a friendly manner.
If you don’t know the answer, ask the user to reach out to the official support team.
"""

# Function to get response from Nova
def ask_nova(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": assistant_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

# Streamlit app
st.set_page_config(page_title="Nova FAQ Assistant", page_icon="🤖")
st.title("📚 Nova - College FAQ Assistant")
st.write("Ask me anything about your college rules, facilities, or placements!")

user_input = st.text_input("💬 Type your question here:")

if user_input:
    with st.spinner("Nova is thinking..."):
        answer = ask_nova(user_input)
        st.success("✅ Answer from Nova:")
        st.write(answer)
