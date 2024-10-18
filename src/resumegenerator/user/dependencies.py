from typing import Annotated

from fastapi import Depends, UploadFile
from firebase_admin import auth

from ..auth.dependencies import get_admin, get_current_user
from ..storage.services import store_profile_pic
from .models import User, UserForm


def update_user_record(
    user: Annotated[User, Depends(get_current_user)],
    user_data: UserForm = Depends(),
    profile_pic: UploadFile = None,
) -> User:
    photo_url = None
    if profile_pic:
        photo_url = store_profile_pic(
            user.uid, profile_pic.file, profile_pic.content_type, profile_pic.filename
        )
    user = auth.update_user(user.uid, **user_data.model_dump(), photo_url=photo_url)
    return user
