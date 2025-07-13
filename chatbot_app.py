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

# ✅ Send message function
def send_message():
    user_message = st.session_state.input.strip()
    if user_message:
        st.session_state.messages.append({"role": "user", "content": user_message})

        # Only keep last 10 messages for context if you want faster
        context_messages = st.session_state.messages[-10:]

        response = ollama_client.chat(
            model="phi3",  # Replace with your preferred/fastest model (e.g., "phi3", "llama2:7b" if installed)
            messages=context_messages
        )
        bot_reply = response['message']['content']
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        st.session_state.input = ""  # Clear input

# ✅ Spacer to push input down on mobile
st.markdown("<div style='height:30vh;'></div>", unsafe_allow_html=True)

# ✅ Input + Send button
col1, col2 = st.columns([5, 1])
with col1:
    st.text_input(
        "Ask your MedTech question:",
        key="input",
        on_change=send_message,
        placeholder="Type your question here...",
        label_visibility="collapsed"
    )
with col2:
    if st.button("Send"):
        send_message()
