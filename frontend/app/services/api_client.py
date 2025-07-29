import requests
import streamlit as st
import json
from utils.constants import API_BASE_URL

def get_auth_headers():
    """Constructs authorization headers with the user's ID token."""
    token = st.session_state.get('id_token')
    if not token:
        st.error("Authentication token not found. Please log in.")
        st.stop()
    return {"Authorization": f"Bearer {token}"}

# --- Conversation Endpoints ---

def fetch_conversations():
    """Fetches all conversations for the current user."""
    try:
        response = requests.get(f"{API_BASE_URL}/conversations/", headers=get_auth_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching conversations: {e}")
        return []

def create_new_conversation(title: str):
    """Creates a new conversation."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/conversations/",
            json={"title": title},
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error creating conversation: {e}")
        return None

def rename_conversation(conv_id: str, new_title: str):
    """Renames a conversation."""
    try:
        response = requests.put(
            f"{API_BASE_URL}/conversations/{conv_id}",
            json={"title": new_title},
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error renaming conversation: {e}")
        return False

def delete_conversation(conv_id: str):
    """Deletes a conversation."""
    try:
        response = requests.delete(f"{API_BASE_URL}/conversations/{conv_id}", headers=get_auth_headers())
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting conversation: {e}")
        return False

# --- Chat Endpoints ---

def fetch_messages(conv_id: str):
    """
    Fetches all messages for a given conversation.
    NOTE: This is not implemented in the backend API as we use LangChain's memory.
    This function is a placeholder for a potential future implementation.
    The current approach rebuilds the message list from the Firestore-backed history.
    """
    # This is a conceptual function. In our current design, history is loaded
    # via LangChain's memory service on the backend, not via a separate message API endpoint.
    # We rebuild it on the frontend by re-playing the conversation.
    return []


def stream_chat_responses(conv_id: str, message: str):
    """
    Sends a message and streams the response from the backend.
    This is a generator function that yields content chunks.
    """
    payload = {"conversation_id": conv_id, "message": message}
    try:
        with requests.post(f"{API_BASE_URL}/chat/message", json=payload, headers=get_auth_headers(), stream=True) as r:
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
                            print(f"Could not decode JSON from chunk: {data_str}")
                            continue
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while communicating with the chat API: {e}")
        yield ""