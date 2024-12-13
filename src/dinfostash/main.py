from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from dinfostash.auth.routes import router as auth_router
from dinfostash.data.router import router as data_router
from dinfostash.resume.router import router as resume_router
from dinfostash.user.router import router as user_router

app = FastAPI(
    title="DinfoStash",
    summary="A Developer Information Manager that can store and manage developer's portfolio data and also generate resumes.",
)
app.include_router(auth_router)
app.include_router(data_router)
app.include_router(resume_router)
app.include_router(user_router)


app.mount(
    "/static",
    StaticFiles(directory="src/dinfostash/static"),
    name="static",
)

favicon_path = "src/dinfostash/static/logo.ico"


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(favicon_path)
