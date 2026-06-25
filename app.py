import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Hadie's AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f0f4ff, #e8f0fe, #f5f0ff);
        background-attachment: fixed;
    }
    .block-container {
        padding-top: 2rem;
    }
    .title-style {
        text-align: center;
        background: linear-gradient(90deg, #7c3aed, #4f46e5, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px;
        font-weight: 900;
        margin-bottom: 0px;
        letter-spacing: 2px;
    }
    .subtitle-style {
        text-align: center;
        color: #7c3aed;
        font-size: 16px;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }
    .glow-divider {
        height: 2px;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #f472b6);
        border: none;
        border-radius: 10px;
        margin: 10px 0 20px 0;
    }
    .stChatMessage {
        border-radius: 20px !important;
        padding: 15px !important;
        margin: 8px 0 !important;
        border: 1px solid rgba(167, 139, 250, 0.3) !important;
    }
    .stChatInput input {
        border-radius: 25px !important;
        border: 2px solid #7c3aed !important;
        padding: 15px 20px !important;
        font-size: 15px !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ede9fe, #ddd6fe) !important;
        border-right: 1px solid rgba(167, 139, 250, 0.3) !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] label {
        color: #1e1b4b !important;
    }
    .stButton button {
        background: linear-gradient(90deg, #7c3aed, #4f46e5) !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #f0f4ff;
    }
    ::-webkit-scrollbar-thumb {
        background: #7c3aed;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

def speak_text(text):
    js = f"""
    <script>
    var msg = new SpeechSynthesisUtterance();
    msg.text = `{text[:300]}`;
    msg.lang = 'en-US';
    msg.rate = 1.0;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js, height=0)

with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding: 10px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/4712/4712109.png' width='90'/>
            <h2 style='color:#7c3aed; margin-top:10px;'>Hadie's AI Chatbot</h2>
            <p style='color:#4f46e5; font-size:13px;'>Powered by Groq + Llama 3</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#7c3aed;'>", unsafe_allow_html=True)
    st.markdown("### Settings")
    voice_enabled = st.toggle("Voice Reply", value=True)
    st.markdown("<hr style='border-color:#7c3aed;'>", unsafe_allow_html=True)
    st.markdown("### Ask me about:")
    topics = ["General Knowledge", "Science and Tech", "Cooking Recipes",
              "Math Problems", "Urdu and English", "Coding Help",
              "Health Tips", "Travel and Places"]
    for topic in topics:
        st.markdown(f"<p style='margin:2px 0; font-size:14px; color:#1e1b4b;'>{topic}</p>",
                   unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#7c3aed;'>", unsafe_allow_html=True)
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("""
        <div style='text-align:center; margin-top:20px;'>
            <p style='color:#7c3aed; font-size:12px;'>Made with love using Streamlit</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown('<p class="title-style">Hadie AI Chatbot</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-style">Your Personal Free AI Assistant</p>', unsafe_allow_html=True)
st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message("assistant"):
        st.markdown("""
        **Hello! Welcome to Hadie's AI Chatbot!**

        I am your personal AI assistant powered by the latest AI technology!

        I can help you with anything you need:
        - Answer your questions
        - Help you learn new things
        - Give you recipes
        - Help with coding
        - And much more!

        Just type your message below and let's chat!
        """)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
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

    if voice_enabled:
        speak_text(reply)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": reply})
