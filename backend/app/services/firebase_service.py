from firebase_admin import firestore

# This provides a singleton Firestore client instance
db = firestore.client()