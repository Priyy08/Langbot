import streamlit as st
import pyrebase
from utils.constants import FIREBASE_CONFIG

# Initialize Pyrebase
try:
    firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
    auth = firebase.auth()
except Exception as e:
    st.error(f"Failed to initialize Firebase: {e}")
    auth = None

def handle_login(email, password):
    """Handles user login."""
    if not auth: return
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state['logged_in'] = True
        st.session_state['user_info'] = {'email': user['email'], 'uid': user['localId']}
        st.session_state['id_token'] = user['idToken']
        st.success("Logged in successfully!")
        st.rerun()
    except Exception as e:
        st.error("Login failed: Invalid email or password.")

def handle_register(email, password, display_name):
    """Handles user registration."""
    # This calls our backend, which uses the Admin SDK
    from services.api_client import API_BASE_URL # Local import to avoid circular dependency
    import requests
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register", json={
            "email": email,
            "password": password,
            "display_name": display_name
        })
        response.raise_for_status()
        st.success("Registration successful! Please log in.")
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"Registration failed: {e.response.json().get('detail', 'Unknown error')}")
        return False


def handle_logout():
    """Handles user logout."""
    st.session_state['logged_in'] = False
    st.session_state['user_info'] = None
    st.session_state['id_token'] = None
    st.session_state['active_conversation_id'] = None
    st.session_state['conversations'] = []
    st.session_state['messages'] = []
    st.info("You have been logged out.")
    st.rerun()