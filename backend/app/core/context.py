# backend/app/core/context.py
from contextvars import ContextVar
from typing import Optional, Dict, Any

# Create a context variable with a default value of None.
# This will hold the current user's info for a single request.
_user_context: ContextVar[Optional[Dict[str, Any]]] = ContextVar("user_context", default=None)

def set_user_context(user: Dict[str, Any]) -> None:
    """Sets the user context for the current request."""
    _user_context.set(user)

def get_user_context() -> Optional[Dict[str, Any]]:
    """Gets the user context for the current request."""
    return _user_context.get()