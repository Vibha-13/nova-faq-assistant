import streamlit as st
import time

# ------------------ Configuration ------------------
st.set_page_config(page_title="Nova - FAQ Assistant", page_icon="🧠", layout="centered")

# ------------------ Session States ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "mood" not in st.session_state:
    st.session_state.mood = "Assistant"

# ------------------ Nova's Personality ------------------
MOOD_STYLES = {
    "Formal": "I'm here to assist you with accurate and clear answers.",
    "Assistant": "Sure! Here's what I found for you.",
    "Playful": "Oh, you’re in for a ride! Here’s what I’ve got 🎉",
    "Sassy Nova": "Honey, let me fix that for you 💅",
}

def generate_nova_reply(user_msg, mood):
    # 🔮 Mock replies — replace with OpenAI integration later
    if "ai" in user_msg.lower():
        return "AI, or Artificial Intelligence, refers to machines designed to mimic human intelligence—like me 😏"
    elif "net" in user_msg.lower():
        return "NET can refer to many things, but often it stands for 'Network'. In tech, it’s all about connections."
    else:
        return MOOD_STYLES[mood] + f" You asked: *{user_msg}*"

def nova_typing_simulation(response):
    placeholder = st.empty()
    full_text = ""
    for char in response:
        full_text += char
        placeholder.markdown(f"🧠 **Nova**: {full_text}")
        time.sleep(0.02)
    return full_text

# ------------------ UI ------------------
st.title("🧠 Nova - Your FAQ Assistant")

with st.sidebar:
    st.markdown("### 🪄 Choose Nova's Mood")
    mood = st.radio("How should Nova talk today?", list(MOOD_STYLES.keys()))
    st.session_state.mood = mood

st.markdown("Ask me anything related to your FAQ project! 😎")

user_input = st.text_input("📝 Your question", placeholder="e.g., What is AI?")

if st.button("Send") and user_input.strip():
    user_msg = user_input.strip()
    nova_response = generate_nova_reply(user_msg, st.session_state.mood)

    # Append to chat history
    st.session_state.chat_history.append({"user": user_msg, "nova": nova_response})

# ------------------ Chat Display ------------------
for entry in st.session_state.chat_history:
    st.markdown(f"👤 **You**: {entry['user']}")
    nova_typing_simulation(entry["nova"])
