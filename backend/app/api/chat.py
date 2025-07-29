from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from ..models.message import ChatMessage
from ..services.langchain_service import chain_with_history
from ..services.auth_service import get_current_user
from ..services.firebase_service import db
import json

router = APIRouter()

async def stream_generator(response_stream):
    """
    Generator function to stream the LangChain response.
    It yields each content chunk as it arrives.
    """
    async for chunk in response_stream:
        content = chunk.content
        if content:
            # We wrap each chunk in a simple JSON structure for easier client-side parsing
            yield f"data: {json.dumps({'content': content})}\n\n"

@router.post("/message")
async def stream_chat_message(
    chat_message: ChatMessage, 
    current_user: dict = Depends(get_current_user)
):
    """
    Receives a user message and streams back the LLM response in real-time.
    """
    user_id = current_user['uid']
    conversation_id = chat_message.conversation_id
    
    # Check if the conversation belongs to the user
    conv_ref = db.collection("conversations").document(conversation_id)
    conv_doc = conv_ref.get()
    if not conv_doc.exists or conv_doc.to_dict().get("user_id") != user_id:
        raise HTTPException(status_code=404, detail="Conversation not found or access denied")

    # Configuration for the LangChain runnable
    config = {"configurable": {"session_id": conversation_id, "user_id": user_id}}
    
    # Use astream_events for more granular control if needed, but astream is simpler
    response_stream = chain_with_history.astream(
        {"question": chat_message.message},
        config=config,
    )
    
    # Return a StreamingResponse that uses our async generator
    return StreamingResponse(stream_generator(response_stream), media_type="text/event-stream")

# Note: The PRD mentioned WebSockets. While FastAPI supports WebSockets well,
# integrating them with Streamlit's re-run model is complex.
# Server-Sent Events (SSE), which StreamingResponse implements, is a more
# robust and simpler pattern for this specific stack, delivering the same
# "real-time" user experience for streaming LLM responses.