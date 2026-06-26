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
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #9333ea);
        padding: 12px 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(124,58,237,0.4);
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
        padding: 6px 14px;
        border-radius: 20px;
    }
    .navbar-badge {
        background: #f472b6;
        color: white;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
    }
    .block-container {
        padding-top: 90px !important;
        max-width: 800px;
        margin: auto;
    }
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
    .stChatMessage {
        border-radius: 20px !important;
        padding: 15px !important;
        margin: 8px 0 !important;
        border: 1px solid rgba(167,139,250,0.3) !important;
    }
    .stChatInput input {
        border-radius: 25px !important;
        border: 2px solid #7c3aed !important;
        padding: 15px 20px !important;
        font-size: 15px !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ede9fe, #ddd6fe) !important;
        border-right: 1px solid rgba(167,139,250,0.3) !important;
        margin-top: 70px;
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
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f0f4ff; }
    ::-webkit-scrollbar-thumb {
        background: #7c3aed;
        border-radius: 10px;
    }
    </style>

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
    components.html(js, height=0)


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
Be warm, encouraging and supportive."""

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding:10px;'>
            <img src='https://placehold.co/100x100/7c3aed/white?text=H&font=montserrat'
            width='90' style='border-radius:50%;
            box-shadow:0 0 20px rgba(124,58,237,0.5);'/>
            <h2 style='color:#7c3aed; margin-top:10px;'>Hadie's AI</h2>
            <p style='color:#4f46e5; font-size:13px;'>Your Smart Assistant</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#7c3aed;'>", unsafe_allow_html=True)
    st.markdown("### Settings")
    voice_reply = st.toggle("Voice Reply", value=True)
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
            f"<p style='margin:2px 0;font-size:13px;color:#1e1b4b;'>✅ {topic}</p>",
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

# Title
st.markdown('<p class="title-style">Hadie AI Chatbot</p>',
            unsafe_allow_html=True)
st.markdown('<p class="subtitle-style">Your Personal Smart AI Assistant</p>',
            unsafe_allow_html=True)
st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message("assistant",
            avatar="https://placehold.co/100x100/7c3aed/white?text=H&font=montserrat"):
        st.markdown("""
        **Hello! Welcome to Hadie's AI Chatbot!**

        I am your personal smart AI assistant!

        You can **type** your message below OR
        click the **mic button** to speak to me!

        I can help you with anything — just ask!
        """)

# Show chat history
for message in st.session_state.messages:
    avatar = "https://placehold.co/100x100/7c3aed/white?text=H&font=montserrat" \
        if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


# Get AI response
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


# Voice input component
st.markdown("""
    <div style='background:white; border-radius:20px;
    border:2px solid #7c3aed; padding:15px; margin-bottom:15px;
    box-shadow:0 0 15px rgba(124,58,237,0.1);'>
        <p style='color:#7c3aed; font-weight:600;
        font-size:14px; margin:0 0 10px 0;'>
        🎤 Voice Input — Click mic and speak!</p>
""", unsafe_allow_html=True)

components.html("""
    <div style="text-align:center;">
        <button id="micBtn" onclick="toggleRecording()" style="
            background: linear-gradient(90deg, #7c3aed, #4f46e5);
            color: white;
            border: none;
            border-radius: 50px;
            padding: 12px 30px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-bottom: 10px;
        ">🎤 Click to Speak</button>

        <div id="statusText" style="
            color: #7c3aed;
            font-size: 13px;
            margin: 5px 0;
        ">Press the button and speak in English</div>

        <div id="transcriptBox" style="
            background: #f5f0ff;
            border: 1.5px solid #7c3aed;
            border-radius: 12px;
            padding: 10px;
            margin: 8px 0;
            min-height: 35px;
            font-size: 14px;
            color: #1e1b4b;
            display: none;
            text-align: left;
        "></div>

        <button id="sendBtn" onclick="sendMessage()" style="
            display: none;
            background: linear-gradient(90deg, #f472b6, #9333ea);
            color: white;
            border: none;
            border-radius: 50px;
            padding: 10px 30px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-top: 5px;
        ">Send This Message</button>
    </div>

    <script>
    let recognition;
    let isRecording = false;
    let spokenText = '';

    function toggleRecording() {
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
        }
    }

    function startRecording() {
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SR) {
            document.getElementById('statusText').innerText =
                'Please use Google Chrome for voice!';
            return;
        }
        recognition = new SR();
        recognition.lang = 'en-US';
        recognition.interimResults = true;
        recognition.continuous = false;

        recognition.onstart = () => {
            isRecording = true;
            spokenText = '';
            document.getElementById('micBtn').innerText = '🔴 Recording... Click to Stop';
            document.getElementById('micBtn').style.background =
                'linear-gradient(90deg, #ef4444, #dc2626)';
            document.getElementById('statusText').innerText =
                'Listening... speak now!';
            document.getElementById('transcriptBox').style.display = 'block';
            document.getElementById('transcriptBox').innerText = '';
            document.getElementById('sendBtn').style.display = 'none';
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
            document.getElementById('transcriptBox').innerText =
                spokenText || interim;
        };

        recognition.onend = () => {
            isRecording = false;
            document.getElementById('micBtn').innerText = '🎤 Click to Speak Again';
            document.getElementById('micBtn').style.background =
                'linear-gradient(90deg, #7c3aed, #4f46e5)';
            if (spokenText) {
                document.getElementById('statusText').innerText =
                    'Voice captured! Click Send to send your message.';
                document.getElementById('sendBtn').style.display = 'block';
            } else {
                document.getElementById('statusText').innerText =
                    'Did not hear anything. Please try again!';
            }
        };

        recognition.onerror = (event) => {
            isRecording = false;
            document.getElementById('micBtn').innerText = '🎤 Click to Speak';
            document.getElementById('micBtn').style.background =
                'linear-gradient(90deg, #7c3aed, #4f46e5)';
            document.getElementById('statusText').innerText =
                'Error: ' + event.error + '. Try again!';
        };

        recognition.start();
    }

    function stopRecording() {
        if (recognition) recognition.stop();
    }

    function sendMessage() {
        if (spokenText) {
            const input = window.parent.document.querySelector(
                '[data-testid="stChatInput"] textarea'
            );
            if (input) {
                const setter = Object.getOwnPropertyDescriptor(
                    window.HTMLTextAreaElement.prototype, 'value'
                ).set;
                setter.call(input, spokenText);
                input.dispatchEvent(new Event('input', { bubbles: true }));
                setTimeout(() => {
                    input.dispatchEvent(new KeyboardEvent('keydown', {
                        key: 'Enter',
                        code: 'Enter',
                        bubbles: true
                    }));
                }, 300);
                document.getElementById('transcriptBox').innerText = '';
                document.getElementById('sendBtn').style.display = 'none';
                document.getElementById('statusText').innerText =
                    'Message sent! You can speak again.';
                document.getElementById('micBtn').innerText = '🎤 Click to Speak';
                spokenText = '';
            }
        }
    }
    </script>
""", height=220)

st.markdown("</div>", unsafe_allow_html=True)

# Text chat input
if prompt := st.chat_input("Or type your message here..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    get_ai_response(prompt)
    st.rerun()
