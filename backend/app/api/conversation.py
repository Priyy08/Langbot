from fastapi import APIRouter, Depends, HTTPException, status, Response
from ..models.conversation import ConversationCreate, ConversationUpdate, ConversationInDB
from ..services.firebase_service import db
from ..services.auth_service import get_current_user
from typing import List
import datetime

router = APIRouter()

@router.post("/", response_model=ConversationInDB, status_code=status.HTTP_201_CREATED)
async def create_conversation(conv_data: ConversationCreate, current_user: dict = Depends(get_current_user)):
    """
    Create a new chat conversation.
    """
    user_id = current_user['uid']
    timestamp = datetime.datetime.utcnow()
    
    new_conv = {
        "user_id": user_id,
        "title": conv_data.title or "New Conversation",
        "created_at": timestamp,
        "updated_at": timestamp,
        "last_message": None,
        "last_message_timestamp": None,
        "message_count": 0
    }
    
    update_time, conv_ref = db.collection("conversations").add(new_conv)
    
    return ConversationInDB(id=conv_ref.id, **new_conv)


@router.get("/", response_model=List[ConversationInDB])
async def get_conversations(current_user: dict = Depends(get_current_user)):
    """
    Get a list of all conversations for the authenticated user.
    """
    user_id = current_user['uid']
    convs_ref = db.collection("conversations").where("user_id", "==", user_id).order_by("updated_at", direction="DESCENDING").stream()
    
    conversations = []
    for conv in convs_ref:
        conv_dict = conv.to_dict()
        conv_dict['id'] = conv.id
        conversations.append(ConversationInDB.parse_obj(conv_dict))
        
    return conversations

@router.put("/{conversation_id}")
async def update_conversation(conversation_id: str, conv_data: ConversationUpdate, current_user: dict = Depends(get_current_user)):
    """
    Update a conversation's title.
    """
    user_id = current_user['uid']
    conv_ref = db.collection("conversations").document(conversation_id)
    
    # Verify ownership
    conv_doc = conv_ref.get()
    if not conv_doc.exists or conv_doc.to_dict().get("user_id") != user_id:
        raise HTTPException(status_code=404, detail="Conversation not found or access denied")
        
    update_data = conv_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
        
    update_data["updated_at"] = datetime.datetime.utcnow()
    conv_ref.update(update_data)
    
    return {"message": "Conversation updated successfully"}


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(conversation_id: str, current_user: dict = Depends(get_current_user)):
    """
    Delete a conversation and all its messages.
    """
    user_id = current_user['uid']
    conv_ref = db.collection("conversations").document(conversation_id)
    
    # Verify ownership
    conv_doc = conv_ref.get()
    if not conv_doc.exists or conv_doc.to_dict().get("user_id") != user_id:
        raise HTTPException(status_code=404, detail="Conversation not found or access denied")

    # Firestore doesn't have cascading deletes, so we must delete subcollections manually.
    # This is a batch operation for efficiency.
    batch = db.batch()
    
    # Delete messages
    messages_ref = db.collection("messages").where("conversation_id", "==", conversation_id).stream()
    for msg in messages_ref:
        batch.delete(msg.reference)
        
    # Delete the conversation itself
    batch.delete(conv_ref)
    
    batch.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)