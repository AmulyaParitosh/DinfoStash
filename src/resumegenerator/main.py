from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .auth.routes import router as auth_router
from .data.router import router as data_router
from .resume.router import router as resume_router
from .user.router import router as user_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(data_router)
app.include_router(resume_router)
app.include_router(user_router)


app.mount(
    "/static",
    StaticFiles(directory="ResumeGenerator/src/static"),
    name="static",
)
