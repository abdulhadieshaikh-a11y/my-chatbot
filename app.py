import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS decoration
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin: 5px 0;
    }
    .stChatInput input {
        border-radius: 20px;
        border: 2px solid #7c3aed;
        padding: 10px;
    }
    .title-style {
        text-align: center;
        color: #7c3aed;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .subtitle-style {
        text-align: center;
        color: #a78bfa;
        font-size: 16px;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #1e1b4b;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=100)
    st.markdown("## 🤖 My AI Chatbot")
    st.markdown("---")
    st.markdown("### 💡 You can ask me:")
    st.markdown("✅ General knowledge")
    st.markdown("✅ Science & Technology")
    st.markdown("✅ Cooking recipes")
    st.markdown("✅ Math problems")
    st.markdown("✅ Urdu & English help")
    st.markdown("✅ And much more!")
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("Powered by Groq + Llama 3 🚀")

# Main title
st.markdown('<p class="title-style">🤖 My AI Chatbot</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-style">Your personal free AI assistant — ask me anything!</p>', unsafe_allow_html=True)
st.markdown("---")

# Welcome message
if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message("assistant"):
        st.markdown("👋 **Hello! Welcome to My AI Chatbot!**\n\nI am here to help you with anything you need. Just type your question below! 😊")

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("💬 Type your message here..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": reply})
