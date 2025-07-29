import streamlit as st
from utils.state_manager import initialize_session_state
from components.auth_components import show_auth_page
from components.chat_components import show_chat_page

# Set page configuration
st.set_page_config(page_title="Real-Time Chatbot", layout="wide")

def main():
    """Main function to run the Streamlit app."""
    
    # Initialize session state variables if they don't exist
    initialize_session_state()

    # Check if user is logged in
    if not st.session_state.get('logged_in'):
        show_auth_page()
    else:
        # If logged in, show the main chat interface
        show_chat_page()

if __name__ == "__main__":
    main()