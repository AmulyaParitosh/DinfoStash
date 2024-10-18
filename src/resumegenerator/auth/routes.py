from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from firebase_admin import auth

from ..firebase import firebase_app
from .services import sign_in_with_email_and_password

router = APIRouter()


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    sign_in_response = sign_in_with_email_and_password(
        form_data.username, form_data.password
    )
    return {"access_token": sign_in_response.idToken, "token_type": "bearer"}

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))


@router.get("/login", response_class=HTMLResponse)
async def read_item(request: Request):
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    if id_token:
        try:
            claims = auth.verify_id_token(id_token, firebase_app)
        except Exception as exc:
            error_message = str(exc)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user_data": claims,
            "error_message": error_message,
            "token": id_token,
        },
    )
