import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from difflib import SequenceMatcher
import streamlit.components.v1 as components

# ------------------- 🎤 Voice Input (Stable Browser-Based) -------------------
def voice_input():
    st.markdown("### 🎙️ Speak your question")
    components.html(
        """
        <script>
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        function startRecognition() {
            recognition.start();
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                const inputBox = window.parent.document.querySelector('input[type="text"]');
                if (inputBox) inputBox.value = transcript;
                const eventInput = new Event('input', { bubbles: true });
                inputBox.dispatchEvent(eventInput);
            };
        }
        </script>
        <button onclick="startRecognition()">🎤 Click to Speak</button>
        """,
        height=100,
    )

# ------------------- 🧠 API Setup -------------------
api_key = st.secrets["together"]["api_key"]
client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# ------------------- 📁 Load FAQ -------------------
FAQ_FILE = "faqs.csv"
if not os.path.exists(FAQ_FILE):
    st.error("🚨 FAQ file not found! Please ensure 'faqs.csv' is in the app folder.")
    st.stop()

df = pd.read_csv(FAQ_FILE)
faq_qa = list(zip(df["Question"].astype(str), df["Answer"].astype(str)))

# ------------------- 🎨 Page Setup -------------------
st.set_page_config(page_title="Nova - Smart FAQ Assistant", page_icon="🤖", layout="wide")

# ------------------- 📸 Sidebar -------------------
with st.sidebar:
    st.image("nova_bot.png", caption="Nova, your smart assistant 🤖", use_container_width=True)
    st.markdown("### Built by **Solace** & **Nyx** ✨")
    st.markdown("---")
    st.markdown("💬 Ask anything from your FAQ")
    st.markdown("📂 Auto-loads `faqs.csv` from your project")
    st.markdown("🧠 Uses GPT if FAQ match is weak")
    if st.button("🧹 Clear Chat History"):
        st.session_state.history = []

# ------------------- 📜 Chat History Setup -------------------
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🤖 Nova - Smart FAQ Assistant")
st.markdown("#### 💬 Ask your question below or use voice input")

# ------------------- 💬 Input -------------------
user_question = st.text_input("Type your question:")

voice_input()  # 🎤 voice option

# ------------------- 🧠 Match & Respond -------------------
if user_question:
    def similarity(a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    best_match = None
    best_score = 0.0
    for q, a in faq_qa:
        score = similarity(user_question, q)
        if score > best_score:
            best_score = score
            best_match = (q, a)

    if best_score > 0.6:
        response_text = best_match[1]
        st.success(f"✅ Found FAQ Match (Similarity: {best_score:.2f})")
    else:
        st.warning("🤔 No close FAQ match found. Asking GPT instead...")
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are Nova, a helpful and friendly FAQ assistant."},
                    {"role": "user", "content": user_question}
                ]
            )
            response_text = response.choices[0].message.content.strip()
        except Exception as e:
            st.error("❌ GPT failed to respond. Here's the error:")
            st.exception(e)
            response_text = "⚠️ Sorry, something went wrong."

    # Show + store in chat history
    st.session_state.history.append(("🧑 You", user_question))
    st.session_state.history.append(("🤖 Nova", response_text))

# ------------------- 💬 Show Chat History -------------------
if st.session_state.history:
    st.markdown("### 📜 Chat History")
    for sender, message in reversed(st.session_state.history):
        with st.chat_message(sender.split()[1].lower()):
            st.markdown(f"**{sender}**: {message}")
