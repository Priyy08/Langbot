# frontend/app/services/auth_client.py
# REFACTORED VERSION WITHOUT PYREBASE4

import streamlit as st
import requests
from utils.constants import FIREBASE_CONFIG
from services import api_client # We need this for the new logout flow

# --- PYREBASE4 IS NO LONGER USED OR INITIALIZED ---

def handle_login(email, password):
    """Handles user login by calling the Firebase Auth REST API."""
    
    # Get the Web API Key from our config
    api_key = FIREBASE_CONFIG.get("apiKey")
    if not api_key:
        st.error("Firebase API Key is not configured.")
        return

    # Firebase's REST API endpoint for signing in with email/password
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    # Payload to send to the API
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        response = requests.post(rest_api_url, json=payload)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        # If successful, the response contains the user's token and info
        user_data = response.json()
        
        st.session_state['logged_in'] = True
        st.session_state['user_info'] = {'email': user_data.get('email'), 'uid': user_data.get('localId')}
        st.session_state['id_token'] = user_data.get('idToken')
        
        st.success("Logged in successfully!")
        st.rerun()

    except requests.exceptions.HTTPError as e:
        # This will catch errors like "INVALID_PASSWORD" or "EMAIL_NOT_FOUND"
        st.error("Login failed: Invalid email or password.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


def handle_register(email, password, display_name):
    """
    Handles user registration by calling our own backend's /register endpoint.
    This function's logic remains the same as it was already correct.
    """
    try:
        # This function from api_client makes the call to our FastAPI backend
        success = api_client.register_user(email, password, display_name)
        if success:
            st.success("Registration successful! Please log in.")
            return True
        return False # The error is handled inside the api_client function
    except Exception as e:
        st.error(f"An unexpected error occurred during registration: {e}")
        return False

def handle_logout():
    """
    Handles user logout.
    1. Calls the backend to invalidate the token.
    2. Clears the local session state.
    """
    if st.session_state.get('id_token'):
        # Invalidate the token on the backend first
        api_client.logout_user()

    # Clear all local session data
    st.session_state['logged_in'] = False
    st.session_state['user_info'] = None
    st.session_state['id_token'] = None
    st.session_state['active_conversation_id'] = None
    st.session_state['conversations'] = []
    st.session_state['messages'] = []
    
    st.info("You have been logged out.")
    st.rerun()