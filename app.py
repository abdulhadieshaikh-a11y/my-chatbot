import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Beautiful CSS Design
st.markdown("""
    <style>

    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-attachment: fixed;
    }

    /* Main container */
    .block-container {
        padding-top: 2rem;
    }

    /* Title */
    .title-style {
        text-align: center;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 48px;
        font-weight: 900;
        margin-bottom: 0px;
        letter-spacing: 2px;
    }

    /* Subtitle */
    .subtitle-style {
        text-align: center;
        color: #a78bfa;
        font-size: 16px;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }

    /* Glowing divider */
    .glow-divider {
        height: 2px;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #f472b6);
        border: none;
        border-radius: 10px;
        box-shadow: 0 0 10px #a78bfa;
        margin: 10px 0 20px 0;
    }

    /* Chat messages */
    .stChatMessage {
        border-radius: 20px !important;
        padding: 15px !important;
        margin: 8px 0 !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(167, 139, 250, 0.3) !important;
    }

    /* User message */
    [data-testid="stChatMessageContent"] {
        font-size: 15px;
        line-height: 1.6;
    }

    /* Chat input */
    .stChatInput input {
        border-radius: 25px !important;
        border: 2px solid #7c3aed !important;
        background: rgba(255,255,255,0.05) !important;
        color: white !important;
        padding: 15px 20px !important;
        font-size: 15px !important;
        box-shadow: 0 0 15px rgba(124, 58, 237, 0.3) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b, #0f0c29) !important;
        border-right: 1px solid rgba(167, 139, 250, 0.3) !important;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #7c3aed, #4f46e5) !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
        box-shadow: 0 0 15px rgba(124, 58, 237, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }

    .stButton button:hover {
        box-shadow: 0 0 25px rgba(124, 58, 237, 0.7) !important;
        transform: translateY(-2px) !important;
    }

    /* Spinner */
    .stSpinner {
        color: #a78bfa !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0f0c29;
    }
    ::-webkit-scrollbar-thumb {
        background: #7c3aed;
        border-radius: 10px;
    }

    /* Stars animation */
    @keyframes twinkle {
        0% { opacity: 0.3; }
        50% { opacity: 1; }
        100% { opacity: 0.3; }
    }
    .star {
        animation: twinkle 2s infinite;
        color: #a78bfa;
        font-size: 12px;
    }

    </style>
""", unsafe_allow_html=True)

# Voice function
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

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding: 10px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/4712/4712109.png' width='90'/>
            <h2 style='color:#a78bfa; margin-top:10px;'>My AI Chatbot</h2>
            <p style='color:#60a5fa; font-size:13px;'>Powered by Groq + Llama 3</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#7c3aed;'>", unsafe_allow_html=True)

    st.markdown("### ⚙️ Settings")
    voice_enabled = st.toggle("🔊 Voice Reply", value=True)

    st.markdown("<hr style='border-color:#7c3aed;'>", unsafe_allow_html=True)

    st.markdown("### 💡 Ask me about:")
    topics = ["✅ General Knowledge", "✅ Science & Tech", "✅ Cooking Recipes",
              "✅ Math Problems", "✅ Urdu & English", "✅ Coding Help",
              "✅ Health Tips", "✅ Travel & Places"]
    for topic in topics:
        st.markdown(f"<p style='margin:2px 0; font-size:14px;'>{topic}</p>",
                   unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#7c3aed;'>", unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""
        <div style='text-align:center; margin-top:20px;'>
            <p style='color:#6366f1; font-size:12px;'>Made with ❤️ using Streamlit</p>
        </div>
    """, unsafe_allow_html=True)

# Header
st.markdown('<p class="title-style">✨ My AI Chatbot ✨</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-style">🌟 Your Personal Free AI Assistant 🌟</p>',
           unsafe_allow_html=True)
st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

# Welcome message
if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message("assistant"):
        st.markdown("""
        👋 **Hello! Welcome to My AI Chatbot!** 🎉

        I am your personal AI assistant powered by the latest AI technology!

        🌟 I can help you with **anything** you need:
        - 💬 Answer your questions
        - 📚 Help you learn new things
        - 🍳 Give you recipes
        - 💻 Help with coding
        - And much more!

        **Just type your message below and let's chat!** 😊
        """)

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("✨ Type your message here..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
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
