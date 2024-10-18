from typing import Annotated

from fastapi import Depends, HTTPException, status
from firebase_admin import auth
from firebase_admin.auth import UserRecord

from ..firebase import firebase_app
from .constants import oauth2_scheme
from .models import AuthClaims


async def authenticate_with_token(
    id_token: Annotated[str, Depends(oauth2_scheme)]
) -> AuthClaims:

    if not id_token:
        raise ValueError("No token provided")

    try:
        return AuthClaims(**auth.verify_id_token(id_token, firebase_app))
    except ValueError as exc:
        raise ValueError("Unauthorized") from exc


async def get_current_user(
    claims: Annotated[AuthClaims, Depends(authenticate_with_token)]
) -> UserRecord:
    if not claims:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # TODO: get user from firebase_admin.auth.get_user so change var name to user in all the dependencies
    return auth.get_user(claims.user_id)

async def get_admin(
    user: Annotated[UserRecord, Depends(get_current_user)]
)-> UserRecord:
    if not user.custom_claims.get('admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not an admin",
        )
    return user
