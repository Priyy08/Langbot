# backend/app/services/langchain_service.py
# CORRECTED AND SIMPLIFIED VERSION

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from .memory_service import FirestoreChatMessageHistory
from ..config.settings import settings
from ..core.context import get_user_context

# 1. Initialize the LLM (No changes needed here)
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=settings.GOOGLE_API_KEY, temperature=0.7, stream=True)

# 2. Create the Prompt Template (No changes needed here)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful and friendly assistant. Answer the user's questions clearly and concisely."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

# 3. Create the primary Conversation Chain (No changes needed here)
conversation_chain = prompt | llm

# --- THIS IS THE KEY FIX ---
# We are changing how we pass the history factory to the runnable.

# The original get_session_history function is perfect and does NOT need to change.
def get_session_history(session_id: str) -> FirestoreChatMessageHistory:
    """
    Factory function that gets the user_id from the request context.
    """
    user_info = get_user_context()
    if not user_info or "uid" not in user_info:
        raise ValueError("User context is not set or is invalid.")
    
    user_id = user_info["uid"]
    return FirestoreChatMessageHistory(conversation_id=session_id, user_id=user_id)


# 4. Wrap the chain with message history management.
#    The fix is to use a lambda function here. This lambda will receive the
#    session_id from the wrapper and the full 'config' dictionary.
#    We can then extract the user_id from the config and call our factory.
# Wrap the chain with the simplified history factory.
chain_with_history = RunnableWithMessageHistory(
    conversation_chain,
    get_session_history, # Pass the new, simpler function
    input_messages_key="question",
    history_messages_key="history",
)