import streamlit as st
from services import api_client
from services.auth_client import handle_logout

def show_sidebar():
    """Renders the sidebar with conversation list and user controls."""
    with st.sidebar:
        st.title("Conversations")
        
        # New Chat Button
        if st.button("➕ New Chat", use_container_width=True):
            new_conv = api_client.create_new_conversation(title="New Conversation")
            if new_conv:
                # Refresh conversation list and switch to the new one
                st.session_state.conversations = api_client.fetch_conversations()
                st.session_state.active_conversation_id = new_conv['id']
                st.session_state.messages = [] # Clear messages for new chat
                st.rerun()

        st.divider()

        # Display list of conversations
        if st.session_state.conversations:
            for conv in st.session_state.conversations:
                conv_id = conv['id']
                # Highlight the active conversation
                conv_title = conv['title']
                button_type = "primary" if conv_id == st.session_state.active_conversation_id else "secondary"
                
                # Use columns for layout
                col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
                with col1:
                    if st.button(f"{conv_title[:25]}{'...' if len(conv_title)>25 else ''}", key=f"conv_{conv_id}", on_click=switch_conversation, args=(conv_id,), use_container_width=True, type=button_type):
                        pass
                
                with col2:
                    if st.button("✏️", key=f"edit_{conv_id}", help="Rename"):
                        handle_rename(conv_id)

                with col3:
                    if st.button("🗑️", key=f"delete_{conv_id}", help="Delete"):
                        handle_delete(conv_id)
        else:
            st.write("No conversations yet.")

        st.divider()
        
        # User Info and Logout
        user_email = st.session_state.get('user_info', {}).get('email', '')
        st.write(f"Logged in as: {user_email}")
        if st.button("Logout", use_container_width=True):
            handle_logout()

def switch_conversation(conv_id):
    """Callback to switch the active conversation."""
    if st.session_state.active_conversation_id != conv_id:
        st.session_state.active_conversation_id = conv_id
        st.session_state.messages = [] # Clear message history when switching

def handle_rename(conv_id):
    """Handles the logic for renaming a conversation."""
    with st.form(key=f"rename_form_{conv_id}"):
        new_title = st.text_input("New Conversation Title")
        submitted = st.form_submit_button("Rename")
        if submitted and new_title:
            if api_client.rename_conversation(conv_id, new_title):
                st.success("Renamed successfully!")
                st.session_state.conversations = api_client.fetch_conversations()
                st.rerun()

def handle_delete(conv_id):
    """Handles the logic for deleting a conversation."""
    if api_client.delete_conversation(conv_id):
        st.success("Deleted successfully!")
        # If the deleted conversation was the active one, reset it
        if st.session_state.active_conversation_id == conv_id:
            st.session_state.active_conversation_id = None
            st.session_state.messages = []
        st.session_state.conversations = api_client.fetch_conversations()
        st.rerun()