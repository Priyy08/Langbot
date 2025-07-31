# CORRECTED AND FINAL VERSION of auth_service.py

from firebase_admin import auth
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .firebase_service import db

# Use HTTPBearer, which simply looks for a "Bearer <token>" in the Authorization header.
# This is the correct scheme for our use case.
bearer_scheme = HTTPBearer()

def create_firebase_user(email, password, display_name):
    """Creates a user in Firebase Auth and a corresponding document in Firestore."""
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        
        user_data = {
            "email": user.email,
            "display_name": user.display_name,
            "created_at": user.user_metadata.creation_timestamp,
            "last_login": user.user_metadata.last_sign_in_timestamp,
            "is_active": True
        }
        db.collection("users").document(user.uid).set(user_data)
        
        return user
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    """
    Dependency to get the current user from a Firebase ID token.
    Verifies the token and returns the decoded user claims.
    """
    # The token is extracted from the 'credentials' part of the bearer scheme
    token = creds.credentials
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    try:
        # Verify the token with Firebase Admin SDK
        decoded_token = auth.verify_id_token(token, check_revoked=True)
        return decoded_token
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except auth.RevokedIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )