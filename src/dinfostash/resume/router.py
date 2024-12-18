from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from dinfostash.resume.constants import FileResponseData, ResumeTemplateEnum
from dinfostash.resume.dependencies import (
    create_resume,
    template_preview,
    create_tailored_resume,
)
from dinfostash.resume.models import ResumeTemplateMetadata
from dinfostash.resume.resume_templates import ResumeTemplate

router = APIRouter(
    prefix="/resumes",
    tags=["resume"],
    responses={404: {"description": "Not found"}},
)


@router.get("/templates")
async def list_templates() -> list[str]:
    return ResumeTemplate.available_templates()


@router.get("/templates/{template_name}")
async def read_template_metadata(
    template_name: ResumeTemplateEnum,  # type: ignore
) -> ResumeTemplateMetadata:
    try:
        return ResumeTemplate.get_template_metadata(template_name.value)
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err


@router.get("/templates/{template_name}/preview")
async def preview_template(
    template_file: Annotated[FileResponseData, Depends(template_preview)]
) -> FileResponse:
    return FileResponse(
        path=template_file.path,
        media_type=template_file.media_type,
        headers=template_file.headers,
    )


@router.post("")
async def generate_resume(
    resume_file: Annotated[FileResponseData, Depends(create_resume)]
) -> FileResponse:
    return FileResponse(
        path=resume_file.path,
        media_type=resume_file.media_type,
        headers=resume_file.headers,
    )


@router.post("/ai")
async def generate_tailored_resume(
    resume_file: Annotated[FileResponseData, Depends(create_tailored_resume)]
) -> FileResponse:
    return FileResponse(
        path=resume_file.path,
        media_type=resume_file.media_type,
        headers=resume_file.headers,
    )
