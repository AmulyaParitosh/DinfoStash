from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from ..resume.resume_templates import ResumeTemplate
from .constants import FileResponseData, ResumeTemplateEnum
from .dependencies import (
    create_resume_from_data,
    create_resume_from_saved_data,
    template_preview,
)
from .models import ResumeTemplateMetadata

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
    template_name: ResumeTemplateEnum,
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


@router.get("/{template_name}")
async def generate_resume_from_user_resume(
    resume_file: Annotated[FileResponseData, Depends(create_resume_from_saved_data)]
) -> FileResponse:
    return FileResponse(
        path=resume_file.path,
        media_type=resume_file.media_type,
        headers=resume_file.headers,
    )


@router.post("/{template_name}")
async def generate_resume_from_post_data(
    resume_file: Annotated[FileResponseData, Depends(create_resume_from_data)],
) -> FileResponse:
    return FileResponse(
        path=resume_file.path,
        media_type=resume_file.media_type,
        headers=resume_file.headers,
    )
