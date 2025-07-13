import streamlit as st
import ollama

# ✅ Create Ollama client
ollama_client = ollama.Client(host="http://127.0.0.1:11434")

# ✅ Page setup
st.set_page_config(page_title="R.ChatBot", page_icon="🤖", layout="centered")
st.markdown("<h2 style='color:#FC8EAC; font-family: Times New Roman, serif; font-style: italic;'>R.ChatBot</h2>", unsafe_allow_html=True)

# ✅ Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Show past messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<span style='color:#1f77b4; font-weight:bold;'>You:</span><br>{msg['content']}", unsafe_allow_html=True)
    else:
        st.markdown(f"<span style='color:#FC74A6; font-weight:bold;'>R.ChatBot:</span><br>{msg['content']}", unsafe_allow_html=True)

# ✅ Text input
user_input = st.text_input(
    "Ask your MedTech question:",
    placeholder="Type your question here...",
    label_visibility="collapsed"
)

# ✅ Send button
if st.button("Send") and user_input.strip() != "":
    user_message = user_input.strip()

    # Append user message first
    st.session_state.messages.append({"role": "user", "content": user_message})

    # Keep last 10 for context
    context_messages = st.session_state.messages[-10:]

    # Call Ollama with Mistral
    response = ollama_client.chat(
        model="mistral",  # ✅ Use Mistral
        messages=context_messages
    )
    bot_reply = response['message']['content']

    # Append bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # Force rerun to clear input
    st.rerun()
