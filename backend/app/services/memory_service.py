from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from typing import List
from .firebase_service import db
import datetime
from google.cloud import firestore

class FirestoreChatMessageHistory(BaseChatMessageHistory):
    """
    Custom Chat Message History store that uses Google Firestore.
    It stores messages in a 'messages' subcollection within a specific conversation document.
    """
    def __init__(self, conversation_id: str, user_id: str):
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.collection = db.collection("messages")
        
        # Ensure the conversation exists and belongs to the user
        conv_ref = db.collection("conversations").document(self.conversation_id)
        conv_doc = conv_ref.get()
        if not conv_doc.exists:
            raise ValueError(f"Conversation with ID {self.conversation_id} not found.")
        
        if conv_doc.to_dict().get("user_id") != self.user_id:
            raise PermissionError("User does not have access to this conversation.")

    @property
    def messages(self) -> List[BaseMessage]:
        """Retrieve messages from Firestore, ordered by timestamp."""
        message_docs = self.collection.where("conversation_id", "==", self.conversation_id).order_by("timestamp", direction="ASCENDING").stream()
        
        items = []
        for doc in message_docs:
            message_data = doc.to_dict()
            # The 'role' from Firestore needs to be mapped to 'type' for LangChain messages
            message_data['type'] = message_data.pop('role', 'human') # Default to human if role is missing
            message_data.pop('timestamp', None) # Remove timestamp as it's not a direct part of message dict
            items.append(message_data)
            
        return messages_from_dict(items)

    def add_message(self, message: BaseMessage) -> None:
        """Append a message to Firestore."""
        # LangChain message dict has 'type', we store it as 'role' in Firestore
        role = message.type
        content = message.content
        
        self.collection.add({
            "conversation_id": self.conversation_id,
            "role": role,
            "content": content,
            "timestamp": datetime.datetime.utcnow()
        })
        
        # Also update the conversation's last message and timestamp
        conv_ref = db.collection("conversations").document(self.conversation_id)
        conv_ref.update({
            "last_message": content[:100], # Preview
            "last_message_timestamp": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow(),
            "message_count": firestore.Increment(1)
        })


    def clear(self) -> None:
        """Clear all messages from the history in Firestore."""
        docs = self.collection.where("conversation_id", "==", self.conversation_id).stream()
        for doc in docs:
            doc.reference.delete()
        
        # Reset conversation metadata
        conv_ref = db.collection("conversations").document(self.conversation_id)
        conv_ref.update({
            "last_message": None,
            "last_message_timestamp": None,
            "message_count": 0
        })