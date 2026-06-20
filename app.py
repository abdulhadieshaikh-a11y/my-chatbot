import streamlit as st
from groq import Groq

st.set_page_config(page_title="My Chatbot", page_icon="🤖")
st.title("My Free AI Chatbot")
st.caption("Powered by Groq + Llama 3")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({
        "role": "user",
        "content": str(prompt)
    })
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat_history = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=chat_history,
            max_tokens=1024
        )
        reply = response.choices[0].message.content
        st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": str(reply)
    })
