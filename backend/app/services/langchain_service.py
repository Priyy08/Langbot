from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from .memory_service import FirestoreChatMessageHistory
from ..config.settings import settings

# 1. Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", google_api_key=settings.GOOGLE_API_KEY, temperature=0.7, stream=True)

# 2. Create the Prompt Template
# This template structures the input to the LLM.
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful and friendly assistant. Answer the user's questions clearly and concisely."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

# 3. Create the primary Conversation Chain
# This chain combines the prompt, the LLM, and memory.
conversation_chain = prompt | llm

def get_session_history(session_id: str, user_id: str) -> FirestoreChatMessageHistory:
    """
    Factory function to get a Firestore-backed chat history object.
    session_id is the conversation_id.
    """
    return FirestoreChatMessageHistory(conversation_id=session_id, user_id=user_id)


# 4. Wrap the chain with message history management
# This is the final, runnable object that manages the conversation flow.
# It uses the `get_session_history` function to dynamically load the history
# for a given session (conversation_id).
chain_with_history = RunnableWithMessageHistory(
    conversation_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)