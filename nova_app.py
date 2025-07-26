import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="🧠 Nova - FAQ Assistant", layout="centered")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🧠 Nova - Your FAQ Assistant")
    st.markdown("Ask me anything about your project. Nova’s got brains and personality 😎")

    mood = st.radio("Choose Nova’s Mood:", ['Friendly 😄', 'Sassy 💅', 'Formal 🧐'])
    
    if st.button("🧼 Clear Chat"):
        st.session_state.messages = []

# --- FAQ DATABASE ---
faq_data = {
    "what is nova": "Nova is your AI-powered FAQ assistant, built using Streamlit!",
    "how does nova work": "Nova uses Python, Streamlit, and a set of predefined FAQs to answer your questions.",
    "who created nova": "You and your brilliant teammate (aka Nyx 😏).",
    "how to add more faqs": "You can add more by editing the `faq_data` dictionary in the code.",
    "which ai is best for generating pictures": "DALL·E, Midjourney, and Stable Diffusion are popular choices for generating AI images."
}

# --- INITIALIZE CHAT MEMORY ---
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- MOOD-BASED RESPONSE WRAPPER ---
def get_response(user_input):
    question = user_input.strip().lower()
    response = faq_data.get(question)

    if response:
        return response
    else:
        if mood == 'Sassy 💅':
            return f"Honey, I don’t have that answer yet 💁‍♀️ But you asked: *{user_input}*"
        elif mood == 'Formal 🧐':
            return f"I'm sorry, I couldn't find an answer for: *{user_input}*. Please refer to your documentation."
        else:  # Friendly
            return f"Oops! I’m still learning that one 😊 Try another question?"

# --- MAIN CHAT UI ---
st.subheader("💬 Ask your question:")

user_input = st.text_input("👤 You:", key="input")

if user_input:
    st.session_state.messages.append(("user", user_input))
    bot_reply = get_response(user_input)
    st.session_state.messages.append(("nova", bot_reply))

# --- DISPLAY CHAT ---
for sender, msg in st.session_state.messages:
    if sender == "user":
        st.markdown(f"**👤 You:** {msg}")
    else:
        st.markdown(f"**🧠 Nova:** {msg}")
