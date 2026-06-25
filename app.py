import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Hadie's AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
    <style>

    /* Hide default streamlit header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #f0f4ff, #e8f0fe, #f5f0ff);
        background-attachment: fixed;
    }

    /* Beautiful Navbar */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #9333ea);
        padding: 12px 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
    }
    .navbar-logo {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        font-weight: 900;
        color: #7c3aed;
        box-shadow: 0 0 15px rgba(255,255,255,0.5);
    }
    .navbar-title {
        font-size: 22px;
        font-weight: 800;
        color: white;
        letter-spacing: 1px;
        margin-left: 12px;
    }
    .navbar-subtitle {
        font-size: 12px;
        color: #ddd6fe;
        margin-left: 12px;
    }
    .navbar-left {
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .navbar-right {
        display: flex;
        gap: 20px;
        align-items: center;
    }
    .navbar-link {
        color: white;
        font-size: 14px;
        font-weight: 500;
        text-decoration: none;
        padding: 6px 14px;
        border-radius: 20px;
        transition: all 0.3s;
        cursor: pointer;
    }
    .navbar-link:hover {
        background: rgba(255,255,255,0.2);
    }
    .navbar-badge {
        background: #f472b6;
        color: white;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
    }

    /* Push content below navbar */
    .block-container {
        padding-top: 90px !important;
        max-width: 800px;
        margin: auto;
    }

    /* Title */
    .title-style {
        text-align: center;
        background: linear-gradient(90deg, #7c3aed, #4f46e5, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 42px;
        font-weight: 900;
        margin-bottom: 0px;
        letter-spacing: 2px;
    }
    .subtitle-style {
        text-align: center;
        color: #7c3aed;
        font-size: 15px;
        margin-bottom: 10px;
    }
    .glow-divider {
        height: 2px;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #f472b6);
        border: none;
        border-radius: 10px;
        margin: 10px 0 20px 0;
    }

    /* Chat messages */
    .stChatMessage {
        border-radius: 20px !important;
        padding: 15px !important;
        margin: 8px 0 !important;
        border: 1px solid rgba(167, 139, 250, 0.3) !important;
    }

    /* Chat input */
    .stChatInput input {
        border-radius: 25px !important;
        border: 2px solid #7c3aed !important;
        padding: 15px 20px !important;
        font-size: 15px !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ede9fe, #ddd6fe) !important;
        border-right: 1px solid rgba(167, 139, 250, 0.3) !important;
        margin-top: 70px;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] label {
        color: #1e1b4b !important;
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #7c3aed, #4f46e5) !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        font-weight: 600 !important;
        width: 100% !important;
    }

    /* Typing animation */
    .typing-animation {
        display: flex;
        gap: 5px;
        padding: 10px;
        align-items: center;
    }
    .typing-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #7c3aed;
        animation: bounce 1.2s infinite;
    }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f0f4ff; }
    ::-webkit-scrollbar-thumb {
        background: #7c3aed;
        border-radius: 10px;
    }

    </style>

    <!-- Beautiful Navbar -->
    <div class="navbar">
        <div class="navbar-left">
            <div class="navbar-logo">H</div>
            <div>
                <div class="navbar-title">Hadie's AI Chatbot</div>
                <div class="navbar-subtitle">Powered by Groq + Llama 3</div>
            </div>
        </div>
        <div class="navbar-right">
            <span class="navbar-link">Home</span>
            <span class="navbar-link">About</span>
            <span class="navbar-link">Help</span>
            <span class="navbar-badge">FREE</span>
        </div>
    </div>
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

def show_typing():
    st.markdown("""
        <div class="typing-animation">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <span style="color:#7c3aed; font-size:14px; margin-left:5px;">
                Hadie's AI is thinking...
            </span>
        </div>
    """, unsafe_allow_html=True)

SYSTEM_PROMPT = """You are Hadie's AI Assistant — a smart, friendly and helpful AI.
You can help with absolutely everything including:
- General knowledge and facts
- Math problems and calculations
- Science questions
- Coding and programming help
- Cooking recipes
- Health and fitness tips
- Travel information
- Urdu and English language help
- Hard and complex questions
- History and geography
- Business and finance advice
- Islamic knowledge
- And absolutely anything else!
Always give clear, helpful and friendly answers.
If someone asks a hard question, think carefully and give the best answer.
Be warm, encouraging and supportive."""

with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding: 10px;'>
            <img src='https://placehold.co/100x100/7c3aed/white?text=H&font=montserrat'
            width='90' style='border-radius:50%;
            box-shadow: 0 0 20px rgba(124,58,237,0.5);'/>
            <h2 style='color:#7c3aed; margin-top:10px;'>Hadie's AI</h2>
            <p style='color:#4f46e5; font-size:13px;'>Your Smart Assistant</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#7c3aed;'>", unsafe_allow_html=True)
    st.markdown("### Settings")
    voice_enabled = st.toggle("Voice Reply", value=True)
    st.markdown("<hr style='border-color:#7c3aed;'>", unsafe_allow_html=True)

    st.markdown("### I can help you with:")
    topics = [
        "General Knowledge",
        "Math and Calculations",
        "Science Questions",
        "Coding and Programming",
        "Cooking Recipes",
        "Health and Fitness",
        "Travel Information",
        "Urdu and English Help",
        "Islamic Knowledge",
        "Business and Finance",
        "Hard and Complex Questions",
        "And Much More!"
    ]
    for topic in topics:
        st.markdown(
            f"<p style='margin:2px 0; font-size:13px;"
            f"color:#1e1b4b;'>✅ {topic}</p>",
            unsafe_allow_html=True
        )

    st.markdown("<hr style='border-color:#7c3aed;'>", unsafe_allow_html=True)
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("""
        <div style='text-align:center; margin-top:20px;'>
            <p style='color:#7c3aed; font-size:12px;'>Made with love by Hadie</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown('<p class="title-style">Hadie AI Chatbot</p>',
           unsafe_allow_html=True)
st.markdown('<p class="subtitle-style">Your Personal Smart AI Assistant</p>',
           unsafe_allow_html=True)
st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message("assistant",
        avatar="https://placehold.co/100x100/7c3aed/white?text=H&font=montserrat"):
        st.markdown("""
        **Hello! Welcome to Hadie's AI Chatbot!**

        I am your personal smart AI assistant!
        I can help you with **anything** you need:

        - General knowledge and facts
        - Math and science questions
        - Coding and programming
        - Cooking recipes
        - Health and fitness tips
        - Islamic knowledge
        - Hard and complex questions
        - And absolutely anything else!

        **Just type your question below — I am ready to help!**
        """)

for message in st.session_state.messages:
    avatar = "https://placehold.co/100x100/7c3aed/white?text=H&font=montserrat" \
        if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    with st.chat_message("assistant",
        avatar="https://placehold.co/100x100/7c3aed/white?text=H&font=montserrat"):
        typing_placeholder = st.empty()
        with typing_placeholder:
            show_typing()

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *[{"role": m["role"], "content": m["content"]}
                  for m in st.session_state.messages],
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048
        )
        reply = response.choices[0].message.content
        typing_placeholder.empty()
        st.markdown(reply)

    if voice_enabled:
        speak_text(reply)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": reply})
