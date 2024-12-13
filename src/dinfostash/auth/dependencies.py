from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from firebase_admin import auth
from firebase_admin.auth import UserRecord

from dinfostash.auth.constants import oauth2_scheme
from dinfostash.auth.models import AuthClaims
from dinfostash.firebase import firebase_app


async def authenticate_with_token(
    id_token: Annotated[str, Depends(oauth2_scheme)]
) -> AuthClaims:

    if not id_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not Found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        return AuthClaims(**auth.verify_id_token(id_token, firebase_app))
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        ) from exc


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
) -> UserRecord:
    if not user.custom_claims.get("admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not an admin",
        )
    return user


async def get_optional_current_user(
    id_token: Annotated[Optional[str], Depends(oauth2_scheme)] = None
) -> Optional[UserRecord]:
    if not id_token:
        return None  # User is not authenticated
    try:
        claims = AuthClaims(**auth.verify_id_token(id_token, firebase_app))
        return auth.get_user(claims.user_id)
    except Exception:
        return None
