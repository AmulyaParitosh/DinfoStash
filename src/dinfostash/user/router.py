from typing import Annotated

from fastapi import APIRouter, Depends, status

from ..auth.dependencies import get_current_user
from .dependencies import update_user_record
from .models import User

router = APIRouter(
    prefix="/user", tags=["user"], responses={404: {"description": "Not found"}}
)


@router.get("/")
def user_data(user: Annotated[User, Depends(get_current_user)]) -> User:
    return user



@router.patch("/", status_code=status.HTTP_200_OK)
def update_user_data(user: Annotated[User, Depends(update_user_record)]) -> User:
    return user
