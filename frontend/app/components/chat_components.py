import streamlit as st
from components.sidebar_components import show_sidebar
from services import api_client

def show_chat_page():
    """
    Renders the main chat interface, including the sidebar and chat window.
    """
    # Fetch conversations on first load after login
    if not st.session_state.get('conversations'):
        st.session_state.conversations = api_client.fetch_conversations()
        # If no active conversation, select the most recent one
        if not st.session_state.active_conversation_id and st.session_state.conversations:
            st.session_state.active_conversation_id = st.session_state.conversations[0]['id']

    # Display sidebar
    show_sidebar()

    # Main chat area
    if not st.session_state.active_conversation_id:
        st.info("Select a conversation or create a new one to start chatting.")
        return

    # Display existing messages for the active conversation
    # The 'messages' in session_state acts as our frontend cache for the active chat
    for message in st.session_state.get("messages", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input field
    if prompt := st.chat_input("What would you like to discuss?"):
        # Add user message to the chat history and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get and display assistant's response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Stream the response from the API
            response_generator = api_client.stream_chat_responses(
                conv_id=st.session_state.active_conversation_id,
                message=prompt
            )

            for chunk in response_generator:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌") # Add a blinking cursor effect
            
            message_placeholder.markdown(full_response)
        
        # Add the complete assistant response to the session's message history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Refresh sidebar to show updated last message timestamp
        st.session_state.conversations = api_client.fetch_conversations()