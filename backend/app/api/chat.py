# backend/app/api/chat.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from ..models.message import ChatMessage
from ..services.langchain_service import chain_with_history
from ..services.auth_service import get_current_user
from ..services.firebase_service import db
import json

# --- Add this new import ---
from ..core.context import set_user_context,get_user_context
# ---------------------------

router = APIRouter()

# --- Create a new dependency ---
def set_context_dependency(current_user: dict = Depends(get_current_user)) -> None:
    """A dependency that sets the user context and does nothing else."""
    set_user_context(current_user)
# -----------------------------

async def stream_generator(response_stream):
    # ... (this function does not change)
    async for chunk in response_stream:
        content = chunk.content
        if content:
            yield f"data: {json.dumps({'content': content})}\n\n"

@router.post("/message")
async def stream_chat_message(
    chat_message: ChatMessage,
    # --- Add the new dependency to the endpoint ---
    # This will run BEFORE the main body of the function.
    context: None = Depends(set_context_dependency)
):
    # ... (rest of the function, but with one change)
    
    # We no longer need the user from get_current_user here, 
    # as it's handled by the dependency.

    conversation_id = chat_message.conversation_id
    
    # Check if the conversation belongs to the user (optional but good practice)
    # This part requires the user_id, which we can still get from the dependency.
    user_info = get_user_context()
    if not user_info:
        raise HTTPException(status_code=401, detail="Could not identify user from token.")
    user_id = user_info['uid']

    conv_ref = db.collection("conversations").document(conversation_id)
    conv_doc = conv_ref.get()
    if not conv_doc.exists or conv_doc.to_dict().get("user_id") != user_id:
        raise HTTPException(status_code=404, detail="Conversation not found or access denied")

    # The config only needs the session_id. The user_id is now in the context.
    config = {"configurable": {"session_id": conversation_id}}
    
    response_stream = chain_with_history.astream(
        {"question": chat_message.message},
        config=config,
    )
    
    return StreamingResponse(stream_generator(response_stream), media_type="text/event-stream")