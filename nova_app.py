import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="🧠 Nova - FAQ Assistant", layout="centered")

# --- SIDEBAR ---
st.sidebar.title("⚙️ Settings")
mood = st.sidebar.radio("Choose Nova’s Mood", ["friendly", "sassy", "professional", "funny"])

# --- TITLE ---
st.markdown("<h1 style='text-align:center;'>🧠 Nova - Your FAQ Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Ask me anything about your project. Nova’s got brains and personality 😎</h4>", unsafe_allow_html=True)
st.markdown("---")

# --- SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- CLEAR CHAT ---
if st.button("🧼 Clear Chat"):
    st.session_state.chat_history = []
    st.experimental_rerun()

# --- USER INPUT ---
user_input = st.text_input("💬 Ask your question:")

# --- FUNCTION: NOVA’S REPLY ---
def get_nova_response(query, mood):
    query_lower = query.lower()

    if "nova" in query_lower:
        response = f"Nova is your personal FAQ Assistant, designed to help you with your project queries. 🧠"
    elif "ai" in query_lower and "image" in query_lower:
        response = "There are several AIs like DALL·E, Midjourney, and Stable Diffusion that are great for generating images!"
    elif "your name" in query_lower or "who are you" in query_lower:
        response = "I’m Nova 💫 — your smart, stylish FAQ assistant!"
    else:
        response = "I'm still learning, but I’ll try my best to help!"

    # Mood styling
    if mood == "sassy":
        response = f"💅 Honey, let me fix that for you — You asked: *{query}* → {response}"
    elif mood == "friendly":
        response = f"😊 Sure! You asked: *{query}* → {response}"
    elif mood == "professional":
        response = f"📘 You asked: *{query}* → {response}"
    elif mood == "funny":
        response = f"😂 Sooo... you want to know: *{query}*? Here you go: {response}"
    
    return response

# --- PROCESS INPUT ---
if user_input:
    nova_reply = get_nova_response(user_input, mood)
    st.session_state.chat_history.append(("👤 You", user_input))
    st.session_state.chat_history.append(("🧠 Nova", nova_reply))

# --- DISPLAY CHAT HISTORY ---
for sender, msg in st.session_state.chat_history:
    with st.chat_message("user" if "You" in sender else "assistant"):
        st.markdown(f"**{sender}:** {msg}")
