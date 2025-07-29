import firebase_admin
from firebase_admin import credentials, firestore, auth
from .settings import settings
import os

def initialize_firebase():
    """
    Initializes the Firebase Admin SDK.
    It checks if the app is already initialized to prevent errors.
    """
    if not firebase_admin._apps:
        # The GOOGLE_APPLICATION_CREDENTIALS env var should be set.
        # It points to the service account key file.
        cred = credentials.ApplicationDefault()
        
        firebase_admin.initialize_app(cred, {
            'projectId': settings.FIREBASE_PROJECT_ID,
        })
    
    print("Firebase App Initialized.")

# You can also export db and auth clients for easy access elsewhere
# but it's cleaner to get them after initialization.
# db = firestore.client()
# auth_client = auth