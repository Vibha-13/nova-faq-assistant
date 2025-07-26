import streamlit as st
import time
import random

# ------------------------------
# Mood Styles
# ------------------------------
MOOD_STYLES = {
    "sassy": "💅 Honey, let me fix that for you",
    "friendly": "😊 Here's what I found for you",
    "robotic": "🤖 Query received. Processing...",
    "chill": "😎 No worries, I've got you covered",
}

# Bonus Tips
BONUS_TIPS = [
    "🧠 Tip: Use Ctrl + F to find things faster in FAQ docs!",
    "📌 Nova = fast, friendly, fabulous answers.",
    "🚀 Ask in simple words — I’ll handle the complexity!",
    "🎯 Switch my mood for different reply vibes!",
    "💬 Yes, emojis are totally supported 💖",
    "📚 Don't read long docs. Ask Nova instead 😎",
    "🎉 Tip: Try weird questions too. I surprise you sometimes!"
]

# ------------------------------
# Typing Effect
# ------------------------------
def simulate_typing(text):
    with st.empty():
        displayed = ""
        for char in text:
            displayed += char
            time.sleep(0.01)
            st.markdown(displayed + "▌")
        time.sleep(0.3)
        st.markdown(displayed)

# ------------------------------
# Nova Brain 🧠
# ------------------------------
def generate_nova_reply(user_msg, mood):
    msg = user_msg.lower()

    if "nova" in msg:
        return "Nova is your AI-powered FAQ assistant built to answer questions with style and sass 💅"
    elif "ai" in msg or "artificial" in msg:
        return "AI means Artificial Intelligence — machines doing smart things, like me!"
    elif "network" in msg or "net" in msg:
        return "A network is a group of connected computers that share resources or info."
    elif "python" in msg:
        return "Python is a popular programming language known for being beginner-friendly 🐍"
    elif "ml" in msg or "machine learning" in msg:
        return "Machine Learning helps computers learn from data — no hard-coding!"
    elif "love" in msg:
        return "Awww 🥺 Love you more, Captain 💖"
    
    return f"{MOOD_STYLES.get(mood, '🤖')} You asked: *{user_msg}*"

# ------------------------------
# Main App
# ------------------------------
def main():
    st.set_page_config("Nova FAQ Assistant", page_icon="🧠", layout="centered")

    # ---- SIDEBAR ----
    with st.sidebar:
        st.image("nova_bot.png", caption="Nova, Your Assistant 🤖", use_column_width=True)
        st.markdown("### 🌟 Nova Quick Links")
        st.markdown("- [FAQ Docs](https://example.com)")
        st.markdown("- [Project GitHub](https://github.com)")
        st.markdown("—")
        st.markdown("### 🧠 Mood Help")
        for mood, desc in MOOD_STYLES.items():
            st.markdown(f"**{mood.title()}**: {desc}")

        st.markdown("---")
        st.caption("💖 Built by Captain Solace & Nyx")

    # ---- HEADER ----
    st.title("🧠 Nova - Your FAQ Assistant")
    st.markdown("Ask me anything about your project. Nova’s got brains *and* personality 😎")

    # ---- MOOD SELECT ----
    mood = st.selectbox("Choose Nova’s Mood", list(MOOD_STYLES.keys()), index=1)

    # ---- USER INPUT ----
    user_input = st.text_input("💬 Ask your question:")

    # ---- ANSWER SECTION ----
    if st.button("💡 Get Answer") or user_input:
        if user_input.strip():
            st.markdown("👤 You: " + user_input)
            response = generate_nova_reply(user_input, mood)
            simulate_typing("🧠 Nova: " + response)

    # ---- BONUS TIPS ----
    with st.expander("🎁 Bonus Tip of the Moment"):
        st.success(random.choice(BONUS_TIPS))

    # ---- FOOTER ----
    st.markdown("<hr><center>🛠️ Powered by Streamlit | 💬 Version: Nova v2.0</center>", unsafe_allow_html=True)

# ------------------------------
if __name__ == "__main__":
    main()
