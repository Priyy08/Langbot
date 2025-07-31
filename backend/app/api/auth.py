# backend/app/api/auth.py
# CORRECTED AND SIMPLIFIED VERSION

from fastapi import APIRouter, Depends, HTTPException, status
from ..models.user import UserCreate  # UserLogin is no longer needed here
from ..services.auth_service import create_firebase_user, get_current_user
from firebase_admin import auth

# --- DELETED SECTION ---
# We remove all imports and initializations related to `pyrebase`,
# `settings`, and the `firebase_config` dictionary. The backend
# does not need these client-side configurations.
# import pyrebase
# from ..config.settings import settings
# -----------------------

router = APIRouter()

# --- THE LOGIN ENDPOINT IS REMOVED ---
# The responsibility of logging in a user (exchanging email/password for a token)
# belongs to the frontend client. The frontend will communicate directly with
# Firebase Authentication services for this. The backend's role is to
# protect its own endpoints by validating the token the frontend provides.

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user using the secure Admin SDK.
    This is a backend responsibility because it involves creating a new user record.
    """
    try:
        user = create_firebase_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.display_name
        )
        return {"message": "User created successfully", "uid": user.uid}
    except HTTPException as e:
        # Re-raise known HTTP exceptions
        raise e
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Log out a user by revoking their refresh tokens via the Admin SDK.
    This is a secure backend operation.
    """
    try:
        auth.revoke_refresh_tokens(current_user['uid'])
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to log out: {e}")


@router.get("/me", summary="Get current user info")
async def get_user_me(current_user: dict = Depends(get_current_user)):
    """
    Get the current authenticated user's profile from their token.
    This is a protected endpoint that implicitly verifies the token's validity.
    It's useful for the frontend to check if its stored token is still active.
    """
    return {"uid": current_user['uid'], "email": current_user.get('email')}