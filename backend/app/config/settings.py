import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID")
    # GOOGLE_APPLICATION_CREDENTIALS is read automatically by the google-cloud library

settings = Settings()