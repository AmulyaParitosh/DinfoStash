from typing import Annotated

from fastapi import APIRouter, Depends, status

from .dependencies import (
    delete_resume,
    get_all_resume,
    get_resume,
    patch_resume,
    post_resume,
)
from .models import ResumeData

router = APIRouter(
    prefix="/data",
    tags=["data"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def all_resumes(
    resume_names: Annotated[list[str], Depends(get_all_resume)]
) -> list[str]:
    return resume_names


@router.get("/{resume_name}")
async def resume_by_name(
    resume: Annotated[ResumeData, Depends(get_resume)]
) -> ResumeData:
    return resume


@router.post("/{resume_name}", status_code=status.HTTP_201_CREATED)
async def create_new_resume_by_name(
    posted_resume: Annotated[ResumeData, Depends(post_resume)],
) -> ResumeData:
    return posted_resume


@router.patch("/{resume_name}", status_code=status.HTTP_200_OK)
async def update_resume_by_name(
    patched_resume: Annotated[ResumeData, Depends(patch_resume)],
) -> ResumeData:
    return patched_resume


@router.delete("/{resume_name}", status_code=status.HTTP_200_OK)
async def remove_resume_by_name(
    removed_at_time: Annotated[str, Depends(delete_resume)]
) -> dict[str, str]:
    return {"deleted_at": removed_at_time}
