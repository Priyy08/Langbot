# Real-Time Chatbot with LangChain and Persistent Storage

This project implements a real-time chatbot application as specified in the accompanying Product Requirements Document (PRD). It features a Streamlit frontend, a FastAPI backend, and uses Firebase for authentication and persistent data storage. Conversations are powered by Google's Gemini LLM via the LangChain framework.

## Features

- **User Authentication**: Secure user registration, login, and session management via Firebase Auth.
- **Persistent Conversations**: Chat history is stored in Firestore and persists across sessions.
- **Multi-Conversation Management**: Users can create, rename, delete, and switch between multiple conversations.
- **Real-Time UI**: A dynamic sidebar and chat window that update seamlessly.
- **Context-Aware AI**: LangChain's memory management ensures the chatbot remembers the context of each separate conversation.
- **Streaming Responses**: AI responses are streamed token-by-token for an interactive, real-time feel.

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: Firebase Firestore
- **Authentication**: Firebase Auth
- **LLM Framework**: LangChain
- **LLM**: Google Gemini API
- **Containerization**: Docker & Docker Compose

## Setup and Installation

### 1. Prerequisites

- Docker and Docker Compose installed.
- A Google Cloud Platform project with the Gemini API enabled.
- A Firebase project with Authentication (Email/Password) and Firestore enabled.

### 2. Configuration

**a. Backend Configuration:**

1.  Navigate to the `backend/` directory.
2.  Create a file named `.env`.
3.  Download your Firebase Admin SDK service account key (a JSON file) from your Firebase project settings.
4.  Populate the `.env` file with the following:

    ```env
    # backend/.env
    GOOGLE_API_KEY="your_google_gemini_api_key"
    
    # IMPORTANT: The Firebase Admin SDK uses this environment variable to find your credentials.
    # Set this to the path of your downloaded Firebase service account JSON file.
    # If running with Docker, the path should be relative to the container's filesystem.
    # The provided Dockerfile copies it to /app/firebase_credentials.json.
    GOOGLE_APPLICATION_CREDENTIALS="/app/firebase_credentials.json"
    
    # This is your Firebase Project ID
    FIREBASE_PROJECT_ID="your-firebase-project-id"
    ```

5.  Place your downloaded Firebase service account key JSON file in the `backend/app/config/` directory and **rename it** to `firebase_credentials.json`. The Dockerfile is configured to copy this file.

**b. Frontend Configuration:**

1.  Navigate to the `frontend/app/utils/` directory.
2.  Open the `constants.py` file.
3.  Replace the placeholder Firebase configuration dictionary with your Firebase Web App's configuration keys, which can be found in your Firebase project settings.

### 3. Running the Application

Once the configuration is complete, navigate to the root directory of the project (`chatbot-system/`) and run:

```bash
docker-compose up --build