import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_key = api_key
openai.api_base = "https://openrouter.ai/api/v1"

# App Config
st.set_page_config(page_title="Nova FAQ Assistant", page_icon="🤖", layout="centered", initial_sidebar_state="auto")

# Custom CSS for dark mode
st.markdown("""
    <style>
    body, .stApp {
        background-color: #0e1117;
        color: white;
    }
    .stTextInput > div > div > input {
        color: white;
        background-color: #262730;
    }
    .stSelectbox > div > div > div {
        color: white;
        background-color: #262730;
    }
    .css-1d391kg {
        background-color: #262730;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("assets/nova_bot.png", width=200)
    st.title("🧠 Nova Assistant")
    mood = st.selectbox("Choose Nova's mood:", ["Helpful 😊", "Sassy 💅", "Professional 👔", "Friendly 🤗"])
    st.markdown("Ask any technical or casual question 👇")

# Title
st.title("💬 Nova GPT FAQ Assistant")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Handle user input
user_input = st.text_input("👤 You:", placeholder="Ask me anything...")

def get_nova_response(user_msg, selected_mood):
    prompt = f"""You're Nova, a {selected_mood.lower()} AI assistant. Be brief, helpful, and a bit quirky if needed.\nUser: {user_msg}\nNova:"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Oops! Something went wrong 💔\n\nError: {str(e)}"

# Display chat
if user_input:
    st.session_state.messages.append(("user", user_input))
    with st.spinner("Nova is thinking..."):
        nova_reply = get_nova_response(user_input, mood)
    st.session_state.messages.append(("nova", nova_reply))

# Show chat history
for sender, msg in st.session_state.messages:
    if sender == "user":
        st.markdown(f"👤 **You**: {msg}")
    else:
        st.markdown(f"🧠 **Nova**: {msg}")
