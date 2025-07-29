from fastapi import APIRouter, Depends, HTTPException, status, Response
from ..models.user import UserCreate, UserLogin
from ..services.auth_service import create_firebase_user, get_current_user
from firebase_admin import auth
import pyrebase # Using pyrebase for client-side operations like sign-in

router = APIRouter()

# You need to initialize pyrebase with your web app config
# This is NOT the admin SDK. Get this from Firebase Console > Project Settings > General > Your web app
# In a real app, this config would also be in settings.
firebase_config = {
    "apiKey": "YOUR_WEB_APP_API_KEY", # Replace
    "authDomain": "YOUR_PROJECT_ID.firebaseapp.com", # Replace
    "projectId": "YOUR_PROJECT_ID", # Replace
    "storageBucket": "YOUR_PROJECT_ID.appspot.com", # Replace
    "messagingSenderId": "YOUR_SENDER_ID", # Replace
    "appId": "YOUR_APP_ID", # Replace
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
pyrebase_auth = firebase.auth()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user.
    """
    try:
        user = create_firebase_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.display_name
        )
        return {"message": "User created successfully", "uid": user.uid}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def login(user_data: UserLogin):
    """
    Log in a user and return an ID token.
    """
    try:
        user = pyrebase_auth.sign_in_with_email_and_password(user_data.email, user_data.password)
        # The idToken is the JWT you'll send to the client.
        return {"token": user['idToken'], "uid": user['localId']}
    except Exception as e:
        # Pyrebase raises a generic exception with an error message in its body
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Log out a user by revoking their refresh tokens.
    """
    try:
        auth.revoke_refresh_tokens(current_user['uid'])
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to log out: {e}")

@router.get("/me")
async def get_user_me(current_user: dict = Depends(get_current_user)):
    """
    Get the current authenticated user's profile.
    """
    return {"uid": current_user['uid'], "email": current_user.get('email')}