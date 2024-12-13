import json

import requests

from dinfostash.auth.models import VerifyPasswordResponse
from dinfostash.auth.utils import raise_detailed_error
from dinfostash.config import SETTINGS


def sign_in_with_email_and_password(
    email: str, password: str
) -> VerifyPasswordResponse:
    request_ref = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={SETTINGS.apiKey}"
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    request_object = requests.post(request_ref, headers=headers, data=data, timeout=10)
    raise_detailed_error(request_object)
    return VerifyPasswordResponse(**request_object.json())
