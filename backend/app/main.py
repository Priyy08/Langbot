from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.firebase_config import initialize_firebase
initialize_firebase()
from .api import auth, conversation, chat

app = FastAPI(
    title="Real-Time Chatbot API",
    description="Backend for the LangChain Chatbot with persistent storage.",
    version="1.0.0"
)

# Initialize Firebase Admin SDK on startup


# Configure CORS
origins = [
    "http://localhost:8501",  # Streamlit default port
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(conversation.router, prefix="/api/conversations", tags=["Conversations"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Chatbot API!"}