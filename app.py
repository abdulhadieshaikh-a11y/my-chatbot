import streamlit as st
from groq import Groq
import streamlit.components.v1 as components
from audio_recorder_streamlit import audio_recorder
import io
import hashlib

st.set_page_config(
    page_title="Hadie's AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    * { font-family: 'Inter', sans-serif; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background: #f8f7ff;
    }

    /* NAVBAR */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background: white;
        padding: 0 40px;
        height: 64px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 1px 0 #ede9fe;
    }
    .navbar-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .navbar-logo {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: 900;
        color: white;
    }
    .navbar-name {
        font-size: 16px;
        font-weight: 700;
        color: #1f2937;
    }
    .navbar-sub {
        font-size: 11px;
        color: #9ca3af;
    }
    .navbar-center {
        display: flex;
        gap: 4px;
    }
    .npill {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        color: #6b7280;
        cursor: pointer;
        transition: all 0.2s;
    }
    .npill:hover {
        background: #f5f0ff;
        color: #7c3aed;
    }
    .navbar-right {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .online-badge {
        display: flex;
        align-items: center;
        gap: 6px;
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 12px;
        font-weight: 600;
        color: #16a34a;
    }
    .online-dot {
        width: 7px;
        height: 7px;
        background: #16a34a;
        border-radius: 50%;
        animation: blink 2s infinite;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    .free-badge {
        background: linear-gradient(90deg, #7c3aed, #4f46e5);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 6px 18px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    /* MAIN LAYOUT */
    .block-container {
        padding-top: 80px !important;
        max-width: 760px !important;
        margin: auto;
        padding-bottom: 20px !important;
    }

    /* HERO */
    .hero-wrap {
        text-align: center;
        padding: 30px 20px 20px;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #f5f0ff;
        border: 1px solid #ddd6fe;
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 12px;
        font-weight: 600;
        color: #7c3aed;
        margin-bottom: 16px;
    }
    .hero-title {
        font-size: 38px;
        font-weight: 900;
        background: linear-gradient(135deg, #7c3aed, #4f46e5, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }
    .hero-sub {
        font-size: 15px;
        color: #6b7280;
        margin-bottom: 20px;
        line-height: 1.6;
    }
    .pills-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: center;
        margin-bottom: 24px;
    }
    .skill-pill {
        background: white;
        border: 1px solid #ede9fe;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 12px;
        font-weight: 600;
        color: #5b21b6;
        box-shadow: 0 1px 4px rgba(124,58,237,0.08);
    }
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-bottom: 10px;
    }
    .stat-box {
        text-align: center;
    }
    .stat-num {
        font-size: 24px;
        font-weight: 900;
        background: linear-gradient(90deg, #7c3aed, #4f46e5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-lbl {
        font-size: 11px;
        color: #9ca3af;
        font-weight: 500;
        margin-top: 2px;
    }

    /* DIVIDER */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent,
            #c4b5fd, #93c5fd, #f9a8d4, transparent);
        border: none;
        margin: 4px 0 20px 0;
    }

    /* CHAT MESSAGES */
    .stChatMessage {
        border-radius: 16px !important;
        padding: 14px 18px !important;
        margin: 6px 0 !important;
        border: 1px solid #f3f0ff !important;
        background: white !important;
        box-shadow: 0 1px 6px rgba(124,58,237,0.06) !important;
    }

    /* CHAT INPUT */
    .stChatInput textarea {
        border-radius: 14px !important;
        border: 1.5px solid #ddd6fe !important;
        padding: 14px 18px !important;
        font-size: 14px !important;
        background: white !important;
        box-shadow: 0 2px 8px rgba(124,58,237,0.06) !important;
        transition: border 0.2s !important;
    }
    .stChatInput textarea:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 3px rgba(124,58,237,0.1) !important;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid #f3f0ff !important;
        margin-top: 64px;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #374151 !important;
    }
    .sb-section {
        background: #faf8ff;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
        border: 1px solid #f3f0ff;
    }
    .sb-title {
        font-size: 10px;
        font-weight: 700;
        color: #a78bfa !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 8px;
    }
    .sk-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 6px 10px;
        border-radius: 8px;
        margin-bottom: 3px;
        font-size: 13px;
        color: #374151;
        font-weight: 500;
        background: white;
        border: 1px solid #f3f0ff;
        transition: all 0.15s;
    }
    .sk-item:hover {
        border-color: #ddd6fe;
        background: #faf8ff;
    }

    /* BUTTONS */
    .stButton button {
        background: linear-gradient(90deg, #7c3aed, #4f46e5) !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        width: 100% !important;
        padding: 9px !important;
        transition: opacity 0.2s !important;
    }
    .stButton button:hover {
        opacity: 0.9 !important;
    }

    /* TYPING */
    .typing-wrap {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 4px;
    }
    .typing-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #7c3aed;
        animation: tdot 1.2s infinite;
    }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes tdot {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
        30% { transform: translateY(-6px); opacity: 1; }
    }
    .typing-text {
        font-size: 13px;
        color: #7c3aed;
        font-weight: 500;
    }

    /* VOICE LABEL */
    .voice-label {
        font-size: 10px;
        color: #a78bfa;
        text-align: center;
        font-weight: 600;
        margin-bottom: 2px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* SCROLLBAR */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: #ddd6fe;
        border-radius: 10px;
    }
    </style>

    <div class="navbar">
        <div class="navbar-left">
            <div class="navbar-logo">H</div>
            <div>
                <div class="navbar-name">Hadie's AI</div>
                <div class="navbar-sub">Powered by Groq + Llama 3</div>
            </div>
        </div>
        <div class="navbar-center">
            <div class="npill">🧠 AI</div>
            <div class="npill">💻 Code</div>
            <div class="npill">📐 Math</div>
            <div class="npill">🌍 Knowledge</div>
            <div class="npill">🎤 Voice</div>
        </div>
        <div class="navbar-right">
            <div class="online-badge">
                <div class="online-dot"></div>
                Online
            </div>
            <div class="free-badge">100% FREE</div>
        </div>
    </div>
""", unsafe_allow_html=True)


def speak_text(text):
    clean = text[:300].replace('`', ' ')
    js = f"""
    <script>
    window.speechSynthesis.cancel();
    var msg = new SpeechSynthesisUtterance(`{clean}`);
    msg.lang = 'en-US';
    msg.rate = 0.95;
    msg.pitch = 1.0;
    window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js, height=0)


def show_typing():
    st.markdown("""
        <div class="typing-wrap">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <span class="typing-text">Hadie's AI is thinking...</span>
        </div>
    """, unsafe_allow_html=True)


SYSTEM_PROMPT = """You are Hadie's AI — a brilliant, warm, and professional AI assistant.
You help with everything:
- General knowledge, history, science, geography
- Math problems and step-by-step calculations
- Coding in Python, JavaScript, and any language
- Writing essays, emails, stories, and content
- Cooking recipes and health advice
- Islamic knowledge and guidance
- Business, finance, and career advice
- Urdu and English language help
- Travel recommendations
- Hard and complex questions
Always be clear, friendly, and helpful.
Use bullet points and formatting for clarity.
For code, always use proper code blocks.
Be warm, encouraging, and professional."""

with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding:20px 10px 15px;'>
            <div style='width:70px; height:70px; border-radius:18px;
            background:linear-gradient(135deg,#7c3aed,#4f46e5);
            display:flex; align-items:center; justify-content:center;
            margin:0 auto 12px; font-size:32px; font-weight:900;
            color:white; box-shadow:0 8px 25px rgba(124,58,237,0.35);'>
                H
            </div>
            <div style='font-size:15px; font-weight:700; color:#1f2937;'>
                Hadie's AI</div>
            <div style='font-size:11px; color:#9ca3af; margin-top:3px;'>
                Personal AI Assistant</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style='background:#f0fdf4; border-radius:10px;
        padding:8px 12px; margin-bottom:14px;
        border:1px solid #bbf7d0; display:flex;
        align-items:center; gap:8px;'>
            <span style='color:#16a34a; font-size:16px;'>●</span>
            <span style='color:#15803d; font-size:13px;
            font-weight:600;'>Online and Ready</span>
        </div>
    """, unsafe_allow_html=True)

    voice_reply = st.toggle("🔊 Voice Reply", value=True)

    st.markdown("<div class='sb-section'>", unsafe_allow_html=True)
    st.markdown("<div class='sb-title'>What I Can Do</div>",
                unsafe_allow_html=True)

    skills = [
        ("💻", "Python and Coding"),
        ("📐", "Math and Calculations"),
        ("🔬", "Science and Research"),
        ("✍️", "Writing and Essays"),
        ("🍳", "Cooking Recipes"),
        ("💪", "Health and Fitness"),
        ("🌍", "Travel and Places"),
        ("🕌", "Islamic Knowledge"),
        ("💼", "Business and Finance"),
        ("🗣️", "Urdu and English"),
        ("🧠", "General Knowledge"),
        ("❓", "Hard Questions"),
    ]
    for icon, skill in skills:
        st.markdown(f"""
            <div class='sk-item'>
                <span>{icon}</span>
                <span>{skill}</span>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.last_audio_hash = ""
        st.rerun()

    st.markdown("""
        <div style='text-align:center; margin-top:16px; padding-bottom:10px;'>
            <div style='font-size:11px; color:#d1d5db;'>
                Made with ❤️ by Hadie
            </div>
            <div style='font-size:10px; color:#e5e7eb; margin-top:3px;'>
                Powered by Groq + Llama 3
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="hero-wrap">
        <div class="hero-badge">⚡ Ultra Fast — Powered by Groq AI</div>
        <div class="hero-title">Hadie's AI Chatbot</div>
        <div class="hero-sub">
            Your smart personal AI assistant.<br>
            Ask anything — get instant professional answers.
        </div>
        <div class="pills-row">
            <div class="skill-pill">💻 Write Code</div>
            <div class="skill-pill">📐 Solve Math</div>
            <div class="skill-pill">✍️ Write Essays</div>
            <div class="skill-pill">🔬 Explain Science</div>
            <div class="skill-pill">🍳 Give Recipes</div>
            <div class="skill-pill">🌍 Answer Anything</div>
            <div class="skill-pill">🎤 Voice Input</div>
            <div class="skill-pill">🔊 Voice Reply</div>
        </div>
        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-num">100+</div>
                <div class="stat-lbl">Topics</div>
            </div>
            <div class="stat-box">
                <div class="stat-num">24/7</div>
                <div class="stat-lbl">Available</div>
            </div>
            <div class="stat-box">
                <div class="stat-num">Free</div>
                <div class="stat-lbl">Forever</div>
            </div>
            <div class="stat-box">
                <div class="stat-num">Fast</div>
                <div class="stat-lbl">Replies</div>
            </div>
        </div>
    </div>
    <hr class="divider">
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = ""

if not st.session_state.messages:
    with st.chat_message("assistant",
            avatar="https://placehold.co/100x100/7c3aed/white?text=H&font=montserrat"):
        st.markdown("""
        **Hello! Welcome to Hadie's AI Chatbot!** 👋

        I am your personal smart AI assistant — here to help you
        with **anything** you need!

        **Try asking me something like:**
        - *"Write a Python program that calculates BMI"*
        - *"Explain the theory of relativity simply"*
        - *"Give me a healthy chicken recipe"*
        - *"What is the history of Pakistan?"*

        Type your message below or use the 🎤 mic to speak!
        """)

for message in st.session_state.messages:
    avatar = "https://placehold.co/100x100/7c3aed/white?text=H&font=montserrat" \
        if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


def get_ai_response(user_prompt):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    with st.chat_message("assistant",
            avatar="https://placehold.co/100x100/7c3aed/white?text=H&font=montserrat"):
        ph = st.empty()
        with ph:
            show_typing()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *[{"role": m["role"], "content": m["content"]}
                  for m in st.session_state.messages],
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=2048
        )
        reply = response.choices[0].message.content
        ph.empty()
        st.markdown(reply)
    if voice_reply:
        speak_text(reply)
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt})
    st.session_state.messages.append(
        {"role": "assistant", "content": reply})


col1, col2 = st.columns([9, 1])

with col1:
    prompt = st.chat_input("Ask me anything...")

with col2:
    st.markdown(
        "<div class='voice-label'>🎤 Voice</div>",
        unsafe_allow_html=True
    )
    audio_bytes = audio_recorder(
        text="",
        recording_color="#ef4444",
        neutral_color="#7c3aed",
        icon_name="microphone",
        icon_size="1x",
        pause_threshold=2.0
    )

if audio_bytes:
    audio_hash = hashlib.md5(audio_bytes).hexdigest()
    if audio_hash != st.session_state.last_audio_hash:
        st.session_state.last_audio_hash = audio_hash
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        with st.spinner("Converting your voice to text..."):
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = "voice.wav"
            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file,
                language="en"
            )
            voice_text = transcription.text
            if voice_text:
                with st.chat_message("user"):
                    st.markdown(voice_text)
                get_ai_response(voice_text)
                st.rerun()

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    get_ai_response(prompt)
    st.rerun()
