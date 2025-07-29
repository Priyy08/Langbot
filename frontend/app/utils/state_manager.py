import streamlit as st

def initialize_session_state():
    """
    Initializes all the necessary keys in Streamlit's session state.
    This function is called once at the beginning of the app run.
    """
    # Authentication state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'user_info' not in st.session_state:
        st.session_state['user_info'] = None # e.g., {'uid': '...', 'email': '...'}
    if 'id_token' not in st.session_state:
        st.session_state['id_token'] = None

    # Conversation state
    if 'conversations' not in st.session_state:
        st.session_state['conversations'] = [] # List of conversation dicts from backend
    if 'active_conversation_id' not in st.session_state:
        st.session_state['active_conversation_id'] = None
    
    # Message state for the active conversation
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [] # List of message dicts {'role': 'user'/'assistant', 'content': '...'}