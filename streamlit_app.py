import streamlit as st
from langchain_gigachat import GigaChat
from langchain.schema import HumanMessage, AIMessage
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


st.title("💬 GigaChat AI")
st.write("This is a simple chatbot that uses GigaChat model to generate responses. ")

gigachat_api_key = st.text_input("Введите ваш ключ GigaChat API", type="password")
if not gigachat_api_key:
    st.info("Please add your GigaChat API key to continue.", icon="🗝️")
else:
    client = GigaChat(
        credentials=gigachat_api_key,
        model="GigaChat",
        ca_bundle_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "russian_trusted_root_ca.cer"
        ),
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(message.content)

    if prompt := st.chat_input("Введите запрос"):
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            response = client.invoke(st.session_state.messages)
            assistant_message = response.content
        except Exception as e:
            assistant_message = f"Error: {e}"

        with st.chat_message("assistant"):
            st.markdown(assistant_message)

        st.session_state.messages.append(AIMessage(content=assistant_message))
