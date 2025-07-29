from firebase_admin import auth
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .firebase_service import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_firebase_user(email, password, display_name):
    """Creates a user in Firebase Auth and a corresponding document in Firestore."""
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        
        # Create a user document in Firestore
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

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependency to get the current user from a Firebase ID token.
    Verifies the token and returns the decoded user claims.
    """
    try:
        # The check_revoked=True flag ensures that the token is not from a logged-out session.
        decoded_token = auth.verify_id_token(token, check_revoked=True)
        return decoded_token
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
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