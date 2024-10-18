from calendar import c
from typing import BinaryIO

from .constants import mime, storage_bucket


def store_file(user_id: str, file_name: str, file: bytes, content_type: str = None) -> str:
    blob = storage_bucket.blob(f"{user_id}/{file_name}")
    if not content_type:
        content_type = mime.guess_type(file_name)[0]
    blob.upload_from_file(file, content_type=content_type)
    return blob.public_url


def store_profile_pic(
    user_id: str, file: BinaryIO, content_type: str, filename: str
) -> str:
    blob = storage_bucket.blob(f"profile_photo/{user_id}_{filename}")
    blob.upload_from_file(file, content_type=content_type)
    blob.make_public()
    return blob.public_url


def get_file_url(user_id: str, file_name: str) -> str:
    blob = storage_bucket.blob(f"{user_id}/{file_name}")
    return blob.public_url


def get_profile_pic_url(user_id: str) -> str:
    blob = storage_bucket.blob(f"{user_id}/profile_photo/profile_pic")
    return blob.public_url
