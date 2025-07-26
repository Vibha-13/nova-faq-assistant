import streamlit as st
import openai
import os
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="🧠 Nova - Your FAQ Assistant", page_icon="🧠", layout="centered")

# --- SIDEBAR IMAGE + MOOD ---
with st.sidebar:
    st.image("nova_bot.png", width=200, caption="Nova the Brainy Bot 🧠")
    st.title("🌀 Nova’s Mood")
    mood = st.selectbox("Choose how Nova replies:", ["Friendly", "Sassy", "Professional", "Chill", "Funny"])
    st.markdown("Made with ❤️ by Solace")

# --- TITLE & SUBTITLE ---
st.markdown("## 🧠 Nova - Your FAQ Assistant")
st.markdown("_Ask anything! Nova's got brains, sass, and style 💬_")

# --- OPENAI KEY SETUP ---
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# --- MOOD PROMPTS ---
mood_prompt = {
    "Friendly": "You are Nova, a warm and helpful assistant who explains things kindly like a best friend.",
    "Sassy": "You are Nova, a confident, cheeky AI with a touch of sass. Be bold and witty!",
    "Professional": "You are Nova, a professional expert assistant. Provide clear, formal, accurate explanations.",
    "Chill": "You are Nova, a laid-back, relaxed assistant who speaks like a calm friend.",
    "Funny": "You are Nova, a quirky and funny assistant. Make explanations fun with jokes or emojis!"
}

# --- SESSION CHAT HISTORY ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- GPT RESPONSE ---
def get_nova_response(user_input, mood):
    system_msg = mood_prompt.get(mood, "")
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_input}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.8,
        max_tokens=300
    )
    return response['choices'][0]['message']['content'].strip()

# --- USER INPUT ---
st.markdown("### 💬 Ask your question:")
user_input = st.text_input("👤 You:", key="input_field")

# --- BUTTONS ---
col1, col2 = st.columns([1, 1])
with col1:
    submit = st.button("Ask Nova ✨")
with col2:
    clear = st.button("Clear Chat 🧹")

# --- CLEAR CHAT ---
if clear:
    st.session_state.chat_history = []
    st.experimental_rerun()

# --- PROCESS USER QUERY ---
if submit and user_input:
    nova_reply = get_nova_response(user_input, mood)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Nova", nova_reply))

# --- DISPLAY CHAT ---
for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**👤 You:** {msg}")
    else:
        st.markdown(f"**🧠 Nova:** {msg}")
