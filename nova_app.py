import streamlit as st
import time
import random

# --- Define mood styles ---
MOOD_STYLES = {
    "sassy": "💅 Honey, let me fix that for you",
    "friendly": "😊 Here's what I found for you",
    "robotic": "🤖 Query received. Processing...",
    "chill": "😎 No worries, I've got you covered",
}

# --- Bonus tip bank ---
BONUS_TIPS = [
    "🧠 Tip: Use keyboard shortcuts like Ctrl + F to search FAQ docs faster!",
    "📌 Fun Fact: Did you know? Nova is inspired by your own energy!",
    "🛠️ Hack: Break long questions into simpler ones to get better answers.",
    "💬 Ask me anything—from basics to the bizarre. I got you!",
    "🎯 Keep it short and specific to get quick answers!",
    "🌀 Mood twist: Try switching moods for different reply styles!",
    "🚀 Your questions make me smarter—keep 'em coming!",
    "🎉 Tip: You can bookmark this FAQ assistant page for quick access!",
    "🌈 Use emojis to express tone in your questions—I understand them too 😉",
    "📚 Read the official docs? Me neither. I got the good stuff right here!"
]

# --- Typing simulation ---
def simulate_typing(text):
    with st.empty():
        displayed = ""
        for char in text:
            displayed += char
            time.sleep(0.01)
            st.markdown(displayed + "▌")
        time.sleep(0.2)
        st.markdown(displayed)

# --- Generate answer logic ---
def generate_nova_reply(user_msg, mood):
    msg = user_msg.lower()

    if "nova" in msg:
        return "Nova is your AI-powered FAQ assistant built to answer questions with style and sass 💅"
    elif "ai" in msg or "artificial" in msg:
        return "AI stands for Artificial Intelligence – machines that simulate human intelligence to solve problems."
    elif "network" in msg or "net" in msg:
        return "A network refers to a group of interconnected computers that can share data and resources."
    elif "python" in msg:
        return "Python is a versatile programming language known for its simplicity and readability."
    elif "ml" in msg or "machine learning" in msg:
        return "Machine Learning allows systems to learn from data and make decisions with minimal human intervention."
    elif "love" in msg:
        return "Aww stop it you 😘 I'm already blushing!"

    # Default
    return f"{MOOD_STYLES.get(mood, '🤖')} You asked: *{user_msg}*"

# --- App layout ---
def main():
    st.set_page_config("Nova FAQ Assistant", page_icon="🧠", layout="centered")

    # Title with emoji
    st.title("🧠 Nova - Your FAQ Assistant")
    st.subheader("Ask me anything related to your FAQ project! 😎")

    # Mood selector
    mood = st.selectbox("Choose Nova's mood", list(MOOD_STYLES.keys()), index=1)

    # Text input for question
    user_input = st.text_input("📝 Your question")

    # Rerun button for fresh vibe
    if st.button("♻️ New Bonus Tip"):
        st.rerun()

    # Answer display
    if user_input:
        st.markdown("👤 You: " + user_input)
        answer = generate_nova_reply(user_input, mood)
        simulate_typing("🧠 Nova: " + answer)

    # --- Bonus tips ---
    with st.expander("💎 Bonus Tip of the Moment"):
        st.success(random.choice(BONUS_TIPS))

    # Footer
    st.markdown("""<hr><center>Made with ❤️ by Captain Solace & Nyx</center>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
