from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from dinfostash.auth.routes import router as auth_router
from dinfostash.data.router import router as data_router
from dinfostash.resume.router import router as resume_router
from dinfostash.user.router import router as user_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(data_router)
app.include_router(resume_router)
app.include_router(user_router)


app.mount(
    "/static",
    StaticFiles(directory="src/dinfostash/static"),
    name="static",
)
