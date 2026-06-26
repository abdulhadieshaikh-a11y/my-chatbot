
import streamlit as st
from groq import Groq
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hadie's AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background: linear-gradient(135deg, #f0f4ff, #e8f0fe, #f5f0ff);
        background-attachment: fixed;
    }
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(20px);
        padding: 0 40px;
        height: 65px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 30px rgba(124,58,237,0.15);
        border-bottom: 1px solid rgba(124,58,237,0.1);
    }
    .navbar-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .navbar-logo {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: 900;
        color: white;
        box-shadow: 0 4px 15px rgba(124,58,237,0.4);
    }
    .navbar-brand {
        font-size: 18px;
        font-weight: 800;
        background: linear-gradient(90deg, #7c3aed, #4f46e5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .navbar-tagline {
        font-size: 11px;
        color: #9ca3af;
        margin-top: -2px;
    }
    .navbar-center {
        display: flex;
        gap: 5px;
        align-items: center;
    }
    .navbar-pill {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        color: #6b7280;
        border: 1px solid transparent;
    }
    .navbar-pill:hover {
        background: #f5f0ff;
        color: #7c3aed;
        border-color: #e9d5ff;
    }
    .navbar-right {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        animation: blink 2s infinite;
        display: inline-block;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    .status-text {
        font-size: 12px;
        color: #10b981;
        font-weight: 600;
    }
    .try-btn {
        background: linear-gradient(90deg, #7c3aed, #4f46e5);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 8px 20px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(124,58,237,0.3);
    }
    .hero {
        text-align: center;
        padding: 20px 20px 10px 20px;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #f5f0ff;
        border: 1px solid #e9d5ff;
        border-radius: 20px;
        padding: 5px 15px;
        font-size: 12px;
        font-weight: 600;
        color: #7c3aed;
        margin-bottom: 15px;
    }
    .hero-title {
        font-size: 40px;
        font-weight: 900;
        background: linear-gradient(90deg, #7c3aed, #4f46e5, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 15px;
        color: #6b7280;
        margin-bottom: 20px;
    }
    .caps-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: center;
        margin-bottom: 20px;
    }
    .cap-pill {
        display: flex;
        align-items: center;
        gap: 5px;
        background: white;
        border: 1px solid #e9d5ff;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 12px;
        font-weight: 600;
        color: #4f46e5;
        box-shadow: 0 2px 8px rgba(124,58,237,0.1);
    }
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    .stat-item { text-align: center; }
    .stat-number {
        font-size: 22px;
        font-weight: 900;
        background: linear-gradient(90deg, #7c3aed, #4f46e5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-label {
        font-size: 11px;
        color: #9ca3af;
        font-weight: 500;
    }
    .glow-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent,
            #a78bfa, #60a5fa, #f472b6, transparent);
        border: none;
        margin: 5px 0 15px 0;
    }
    .stChatMessage {
        border-radius: 20px !important;
        padding: 15px !important;
        margin: 8px 0 !important;
        border: 1px solid rgba(167,139,250,0.2) !important;
        background: white !important;
        box-shadow: 0 2px 10px rgba(124,58,237,0.05) !important;
    }
    .stChatInput textarea {
        border-radius: 25px !important;
        border: 2px solid #e9d5ff !important;
        padding: 15px 20px !important;
        font-size: 15px !important;
        background: white !important;
    }
    [data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid #f3f4f6 !important;
        margin-top: 65px;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] label {
        color: #374151 !important;
    }
    .sidebar-section {
        background: #f9fafb;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
        border: 1px solid #f3f4f6;
    }
    .sidebar-title {
        font-size: 11px;
        font-weight: 700;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    .skill-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 7px 10px;
        border-radius: 10px;
        margin-bottom: 4px;
        font-size: 13px;
        color: #374151;
        font-weight: 500;
        background: white;
        border: 1px solid #f3f4f6;
    }
    .skill-icon {
        font-size: 16px;
        width: 24px;
        text-align: center;
    }
    .stButton button {
        background: linear-gradient(90deg, #7c3aed, #4f46e5) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        width: 100% !important;
        padding: 10px !important;
    }
    .typing-animation {
        display: flex;
        gap: 5px;
        padding: 10px;
        align-items: center;
    }
    .typing-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #7c3aed;
        animation: bounce 1.2s infinite;
    }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-8px); }
    }
    .block-container {
        padding-top: 75px !important;
        max-width: 780px;
        margin: auto;
    }
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #f9fafb; }
    ::-webkit-scrollbar-thumb {
        background: #ddd6fe;
        border-radius: 10px;
    }
    </style>

    <div class="navbar">
        <div class="navbar-left">
            <div class="navbar-logo">H</div>
            <div>
                <div class="navbar-brand">Hadie's AI</div>
                <div class="navbar-tagline">Powered by Groq + Llama 3</div>
            </div>
        </div>
        <div class="navbar-center">
            <div class="navbar-pill">🧠 Smart AI</div>
            <div class="navbar-pill">💻 Coding</div>
            <div class="navbar-pill">📐 Math</div>
            <div class="navbar-pill">🌍 Knowledge</div>
            <div class="navbar-pill">🎤 Voice</div>
        </div>
        <div class="navbar-right">
            <span class="status-dot"></span>
            <span class="status-text">Online</span>
            <button class="try-btn">Try Free</button>
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
    components.html(js, height=0)


def show_typing():
    st.markdown("""
        <div class="typing-animation">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <span style="color:#7c3aed; font-size:13px; margin-left:5px;">
                Hadie's AI is thinking...
            </span>
        </div>
    """, unsafe_allow_html=True)


SYSTEM_PROMPT = """You are Hadie's AI Assistant — a smart, friendly and helpful AI.
You can help with absolutely everything including:
- General knowledge and facts
- Math problems and calculations
- Science questions
- Coding and programming help in any language
- Cooking recipes
- Health and fitness tips
- Travel information
- Urdu and English language help
- Hard and complex questions
- History and geography
- Business and finance advice
- Islamic knowledge
- Essay and content writing
- And absolutely anything else!
Always give clear, helpful and friendly answers.
Format code properly with code blocks.
Be warm, encouraging and supportive."""

with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding:15px 10px;'>
            <img src='https://placehold.co/80x80/7c3aed/white?text=H&font=montserrat'
            width='80' style='border-radius:16px;
            box-shadow:0 4px 20px rgba(124,58,237,0.3);'/>
            <div style='font-size:16px; font-weight:800;
            color:#1f2937; margin-top:10px;'>Hadie's AI</div>
            <div style='font-size:12px; color:#9ca3af;'>
            Personal AI Assistant</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style='background:#f0fdf4; border-radius:10px;
        padding:8px 12px; margin-bottom:12px;
        border:1px solid #bbf7d0; display:flex;
        align-items:center; gap:8px;'>
            <span style='color:#10b981; font-size:18px;'>●</span>
            <span style='color:#065f46; font-size:13px;
            font-weight:600;'>AI is Online and Ready</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sidebar-section'>",
                unsafe_allow_html=True)
    st.markdown("<div class='sidebar-title'>Settings</div>",
                unsafe_allow_html=True)
    voice_reply = st.toggle("Voice Reply", value=True)
    st.markdown("</div>", unsafe_allow_html=True)

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

    st.markdown("<div class='sidebar-section'>",
                unsafe_allow_html=True)
    st.markdown("<div class='sidebar-title'>What I Can Do</div>",
                unsafe_allow_html=True)
    for icon, skill in skills:
        st.markdown(f"""
            <div class='skill-item'>
                <span class='skill-icon'>{icon}</span>
                <span>{skill}</span>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""
        <div style='text-align:center; margin-top:15px;'>
            <p style='color:#d1d5db; font-size:11px;'>
            Made with love by Hadie</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="hero">
        <div class="hero-badge">
            <span>⚡</span> Powered by Groq — Ultra Fast AI
        </div>
        <div class="hero-title">Hadie's AI Chatbot</div>
        <div class="hero-subtitle">
            Your professional AI assistant for coding, math,
            writing, and everything else
        </div>
        <div class="caps-row">
            <div class="cap-pill">💻 Write Code</div>
            <div class="cap-pill">📐 Solve Math</div>
            <div class="cap-pill">✍️ Write Essays</div>
            <div class="cap-pill">🔬 Explain Science</div>
            <div class="cap-pill">🍳 Give Recipes</div>
            <div class="cap-pill">🌍 Answer Anything</div>
            <div class="cap-pill">🎤 Voice Input</div>
            <div class="cap-pill">🔊 Voice Reply</div>
        </div>
        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-number">100+</div>
                <div class="stat-label">Topics Covered</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Always Online</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">Free</div>
                <div class="stat-label">No Cost Ever</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">Fast</div>
                <div class="stat-label">Instant Replies</div>
            </div>
        </div>
    </div>
    <hr class="glow-divider">
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message("assistant",
            avatar="https://placehold.co/100x100/7c3aed/white?text=H&font=montserrat"):
        st.markdown("""
        **Hello! Welcome to Hadie's AI Chatbot!**

        I am your personal professional AI assistant!
        I can help you with anything — just ask!

        **Try asking me:**
        - Write a Python program for me
        - Solve this math problem: 25 x 48
        - Explain quantum physics simply
        - Give me a chicken recipe
        - What is the capital of Japan?

        **Type below or click the mic button to speak!**
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
        typing_placeholder = st.empty()
        with typing_placeholder:
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
        typing_placeholder.empty()
        st.markdown(reply)
    if voice_reply:
        speak_text(reply)
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt})
    st.session_state.messages.append(
        {"role": "assistant", "content": reply})


prompt = st.chat_input("Ask me anything...")

components.html("""
    <style>
    .mic-fab {
        position: fixed;
        bottom: 18px;
        right: 18px;
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        border: none;
        cursor: pointer;
        font-size: 20px;
        box-shadow: 0 4px 20px rgba(124,58,237,0.4);
        z-index: 9999;
        transition: all 0.2s;
        color: white;
    }
    .mic-fab:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 25px rgba(124,58,237,0.6);
    }
    .mic-fab.listening {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        animation: ripple 1s infinite;
    }
    @keyframes ripple {
        0% { box-shadow: 0 0 0 0 rgba(239,68,68,0.5); }
        70% { box-shadow: 0 0 0 15px rgba(239,68,68,0); }
        100% { box-shadow: 0 0 0 0 rgba(239,68,68,0); }
    }
    .mic-status {
        position: fixed;
        bottom: 75px;
        right: 10px;
        background: white;
        border: 1px solid #e9d5ff;
        border-radius: 12px;
        padding: 6px 12px;
        font-size: 12px;
        font-weight: 600;
        color: #7c3aed;
        box-shadow: 0 4px 15px rgba(124,58,237,0.15);
        z-index: 9999;
        display: none;
        max-width: 200px;
        text-align: center;
    }
    </style>

    <button class="mic-fab" id="micBtn" onclick="toggleVoice()">🎤</button>
    <div class="mic-status" id="micStatus">Listening...</div>

    <script>
    let recognition;
    let isListening = false;
    let spokenText = '';

    function toggleVoice() {
        if (!isListening) {
            startListening();
        } else {
            stopListening();
        }
    }

    function startListening() {
        const SR = window.SpeechRecognition ||
                   window.webkitSpeechRecognition;
        if (!SR) {
            showStatus('Use Chrome browser!');
            return;
        }
        recognition = new SR();
        recognition.lang = 'en-US';
        recognition.interimResults = true;
        recognition.continuous = false;
        spokenText = '';

        recognition.onstart = () => {
            isListening = true;
            document.getElementById('micBtn').classList.add('listening');
            document.getElementById('micBtn').innerText = '🔴';
            showStatus('Listening... speak now!');
        };

        recognition.onresult = (event) => {
            let interim = '';
            spokenText = '';
            for (let i = 0; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    spokenText += event.results[i][0].transcript;
                } else {
                    interim += event.results[i][0].transcript;
                }
            }
            showStatus(spokenText || interim);
        };

        recognition.onend = () => {
            isListening = false;
            document.getElementById('micBtn').classList.remove('listening');
            document.getElementById('micBtn').innerText = '🎤';
            if (spokenText) {
                showStatus('Sending message...');
                sendToChat(spokenText);
                setTimeout(() => hideStatus(), 2000);
            } else {
                showStatus('Nothing heard. Try again!');
                setTimeout(() => hideStatus(), 2000);
            }
        };

        recognition.onerror = (e) => {
            isListening = false;
            document.getElementById('micBtn').classList.remove('listening');
            document.getElementById('micBtn').innerText = '🎤';
            showStatus('Error: ' + e.error);
            setTimeout(() => hideStatus(), 2000);
        };

        recognition.start();
    }

    function stopListening() {
        if (recognition) recognition.stop();
    }

    function showStatus(text) {
        const s = document.getElementById('micStatus');
        s.innerText = text;
        s.style.display = 'block';
    }

    function hideStatus() {
        document.getElementById('micStatus').style.display = 'none';
    }

    function sendToChat(text) {
        const textarea = window.parent.document.querySelector(
            '[data-testid="stChatInput"] textarea'
        );
        if (textarea) {
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value'
            ).set;
            setter.call(textarea, text);
            textarea.dispatchEvent(new Event('input', { bubbles: true }));
            setTimeout(() => {
                textarea.dispatchEvent(new KeyboardEvent('keydown', {
                    key: 'Enter',
                    code: 'Enter',
                    bubbles: true
                }));
            }, 300);
        }
    }
    </script>
""", height=0)

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    get_ai_response(prompt)
    st.rerun()
