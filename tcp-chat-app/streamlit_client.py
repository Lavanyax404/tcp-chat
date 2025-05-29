import socket
import streamlit as st
import time

# Session state init
if "connected" not in st.session_state:
    st.session_state.connected = False
    st.session_state.client_socket = None
    st.session_state.nickname = ""
    st.session_state.chat_log = []

st.title("💬 TCP Chat Client")

def connect_to_server(nickname):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 5000))
        client.send("NICKNAME".encode())
        client.send(nickname.encode())
        st.session_state.client_socket = client
        st.session_state.connected = True
        st.success("Connected to server!")
    except Exception as e:
        st.error(f"Connection failed: {e}")

if not st.session_state.connected:
    nickname = st.text_input("Enter your nickname:")
    if st.button("Connect"):
        if nickname.strip():
            st.session_state.nickname = nickname.strip()
            connect_to_server(nickname.strip())
        else:
            st.warning("Please enter a valid nickname.")

else:
    with st.form("chat_form"):
        message = st.text_input("Type your message:")
        send_btn = st.form_submit_button("Send")

    client = st.session_state.client_socket

    if send_btn and message.strip():
        try:
            msg_to_send = f"{st.session_state.nickname}: {message}"
            client.send(msg_to_send.encode())
        except Exception as e:
            st.error(f"Failed to send message: {e}")

    # Try receiving new messages
    try:
        client.settimeout(0.2)
        while True:
            try:
                data = client.recv(1024).decode()
                if data:
                    st.session_state.chat_log.append(data)
            except socket.timeout:
                break
    except:
        pass

    # Display chat history
    st.subheader("📝 Chat Log")
    for line in st.session_state.chat_log[-30:]:  # Last 30 messages
        st.markdown(f"🔹 {line}")

    if st.button("Disconnect"):
        client.close()
        st.session_state.connected = False
        st.session_state.chat_log.append("Disconnected.")
        st.rerun()
