import streamlit as st
import openai
import random

st.set_page_config(page_title="Nova", page_icon="🧠", layout="centered")

# --- CSS Styling ---
st.markdown("""
    <style>
    .user-bubble {
        background-color: #f0f0f0;
        color: #111;
        padding: 10px 15px;
        border-radius: 12px;
        margin: 10px 0;
        width: fit-content;
        max-width: 80%;
    }
    .nova-bubble {
        background-color: #f7f0ff;
        color: #222;
        padding: 10px 15px;
        border-radius: 12px;
        margin: 10px 0;
        width: fit-content;
        max-width: 80%;
        align-self: flex-end;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
    }
    .title {
        font-size: 36px;
        font-weight: 700;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 5px;
        color: #7b2cbf;
    }
    .subtitle {
        font-size: 18px;
        text-align: center;
        color: #666;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="title">🧠 Meet Nova</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your cheeky AI sidekick</div>', unsafe_allow_html=True)

# --- Session Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Fun Greeting (only on first visit) ---
if not st.session_state.messages:
    greetings = [
        "Well, well, well, if it isn't boredom knocking at your door. Time to kick boredom to the curb and show it who's boss! What's something fun you can do to shake things up?",
        "I'm not saying I'm a genius, but... actually, yes, I am. Ask away, darling!",
        "Look who decided to chat! What's on your mind, legend?",
        "Nova’s in. Let’s make this conversation sparkle ✨"
    ]
    st.session_state.messages.append(("nova", random.choice(greetings)))

# --- Chat Logic ---
def call_openrouter_gpt(prompt):
    # Replace with your own logic or API call
    # Example placeholder:
    if "chatgpt" in prompt.lower():
        return "Oh, ChatGPT? That's my trusty sidekick. We make quite the dynamic duo, if I do say so myself."
    elif "bored" in prompt.lower():
        return "Time to shake things up! How about you tell me something fun you love doing?"
    else:
        return f"Did someone say \"{prompt}\" or was it just the wind? What can I assist you with today, darling?"

# --- Chat Container Display ---
for role, content in st.session_state.messages:
    bubble_class = "nova-bubble" if role == "nova" else "user-bubble"
    prefix = "🧠 Nova:" if role == "nova" else "🧍‍♂️ You:"
    st.markdown(f'<div class="{bubble_class}">{prefix} {content}</div>', unsafe_allow_html=True)

# --- User Input ---
user_input = st.text_input("Type your question here...", key="input_text")

if user_input:
    st.session_state.messages.append(("user", user_input))
    nova_reply = call_openrouter_gpt(user_input)
    st.session_state.messages.append(("nova", nova_reply))
    st.experimental_rerun()
