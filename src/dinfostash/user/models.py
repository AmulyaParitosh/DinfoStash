from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    uid: str
    email: str
    display_name: str
    email_verified: bool
    disabled: bool
    custom_claims: Optional[dict]
    tokens_valid_after_timestamp: int
    phone_number: Optional[str]
    photo_url: Optional[str]
    provider_id: str
    tenant_id: Optional[str]


class UserForm(BaseModel):
    email: Optional[str] = None
    display_name: Optional[str] = None
    phone_number: Optional[str] = None
