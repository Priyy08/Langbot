import requests
import streamlit as st
import json
from utils.constants import API_BASE_URL

# --- THIS FUNCTION IS CRITICAL ---
def get_auth_headers():
    """Constructs authorization headers with the user's ID token."""
    token = st.session_state.get('id_token')
    
    # This check is important. If there's no token, we can't make authenticated requests.
    if not token:
        st.error("Authentication session has expired. Please log in again.")
        return None
        
    # The header format "Bearer <token>" is a standard requirement for OAuth2/JWT.
    return {"Authorization": f"Bearer {token}"}

# --- CONVERSATION ENDPOINTS (These seem to be working for you) ---

def fetch_conversations():
    """Fetches all conversations for the current user."""
    auth_headers = get_auth_headers()
    if not auth_headers:
        return []
    try:
        response = requests.get(f"{API_BASE_URL}/conversations/", headers=auth_headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching conversations: {e}")
        return []

def create_new_conversation(title: str):
    """Creates a new conversation."""
    auth_headers = get_auth_headers()
    if not auth_headers:
        return None
    try:
        response = requests.post(
            f"{API_BASE_URL}/conversations/",
            json={"title": title},
            headers=auth_headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating conversation: {e}")
        return None

# ... (other conversation functions like rename/delete would follow the same pattern) ...
def rename_conversation(conv_id: str, new_title: str):
    auth_headers = get_auth_headers()
    if not auth_headers: return False
    try:
        response = requests.put(f"{API_BASE_URL}/conversations/{conv_id}", json={"title": new_title}, headers=auth_headers)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error renaming conversation: {e}")
        return False

def delete_conversation(conv_id: str):
    auth_headers = get_auth_headers()
    if not auth_headers: return False
    try:
        response = requests.delete(f"{API_BASE_URL}/conversations/{conv_id}", headers=auth_headers)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting conversation: {e}")
        return False
        
# --- CHAT ENDPOINTS (The source of the error) ---

def stream_chat_responses(conv_id: str, message: str):
    """
    Sends a message and streams the response from the backend.
    """
    payload = {"conversation_id": conv_id, "message": message}
    
    # Step 1: Get the authentication headers.
    auth_headers = get_auth_headers()
    
    # Step 2: If headers are not available (e.g., token expired), stop here.
    if not auth_headers:
        yield ""  # End the generator gracefully
        return

    try:
        # Step 3: **CRITICAL** - Ensure the 'headers=auth_headers' argument is passed to requests.post.
        # This is the line that sends the token to the backend.
        with requests.post(
            f"{API_BASE_URL}/chat/message",
            json=payload,
            headers=auth_headers, 
            stream=True
        ) as r:
            r.raise_for_status()
            for chunk in r.iter_lines():
                if chunk:
                    decoded_chunk = chunk.decode('utf-8')
                    if decoded_chunk.startswith('data:'):
                        try:
                            data_str = decoded_chunk[len('data:'):].strip()
                            data = json.loads(data_str)
                            yield data.get("content", "")
                        except json.JSONDecodeError:
                            continue
                            
    except requests.exceptions.HTTPError as e:
        # This will now properly catch the 401 error and show it to the user.
        st.error(f"An error occurred while communicating with the chat API: {e}")
        yield ""
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        yield ""


# --- Auth Endpoints (These should already be in a different file, but for completeness) ---

def register_user(email: str, password: str, display_name: str):
    """Calls the backend to register a new user."""
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register", json={
            "email": email,
            "password": password,
            "display_name": display_name
        })
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"Registration failed: {e.response.json().get('detail', 'Unknown error')}")
        return False
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the server: {e}")
        return False

def logout_user():
    """Calls the backend to log the user out and invalidate their token."""
    auth_headers = get_auth_headers()
    if not auth_headers:
        return False
    try:
        response = requests.post(f"{API_BASE_URL}/auth/logout", headers=auth_headers)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False
