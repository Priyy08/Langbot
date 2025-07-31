# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Settings:
#     GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
#     FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID")
#     # GOOGLE_APPLICATION_CREDENTIALS is read automatically by the google-cloud library

#     # Firebase Web App Config (for client-side auth)
#     FIREBASE_API_KEY: str = os.getenv("FIREBASE_API_KEY")
#     FIREBASE_AUTH_DOMAIN: str = os.getenv("FIREBASE_AUTH_DOMAIN")
#     FIREBASE_STORAGE_BUCKET: str = os.getenv("FIREBASE_STORAGE_BUCKET")
#     FIREBASE_MESSAGING_SENDER_ID: str = os.getenv("FIREBASE_MESSAGING_SENDER_ID")
#     FIREBASE_APP_ID: str = os.getenv("FIREBASE_APP_ID")
#     FIREBASE_DATABASE_URL: str = os.getenv("FIREBASE_DATABASE_URL", "") # Often optional

# settings = Settings()


# backend/app/settings.py
# Use this simplified version for clarity.

import os
from dotenv import load_dotenv

# This line reads your .env file
load_dotenv()

class Settings:
    # This is for the Gemini LLM
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")

    # This is for the Firebase Admin SDK
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID")

settings = Settings()