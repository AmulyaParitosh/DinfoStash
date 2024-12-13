import mimetypes
import os
import shutil
from typing import Annotated, Optional

from fastapi import BackgroundTasks, Depends, HTTPException, status, Body

from dinfostash.auth.dependencies import get_optional_current_user
from dinfostash.data.dependencies import get_resume
from dinfostash.data.models import ResumeData
from dinfostash.resume.constants import (
    FileResponseData,
    ResumeOutputType,
    ResumeTemplateEnum,
)
from dinfostash.resume.utils import check_image_url
from dinfostash.resume.constants import TempResume
from dinfostash.resume.services import (
    prepare_file_response,
    create_temp_resume_from_data,
)
from dinfostash.user.models import User
from dinfostash.agent.services import tailor_resume


async def template_preview(
    template_name: ResumeTemplateEnum,  # type: ignore
    output_type: ResumeOutputType,
) -> FileResponseData:

    files = [
        f
        for f in os.listdir("example/outputs")
        if f.endswith(output_type.value) and template_name.value in f
    ]

    first_file_path = f"example/outputs/{files[0]}"
    return prepare_file_response(first_file_path, "inline")


async def resume_data(
    user: Optional[User] = Depends(get_optional_current_user),
    resume_name: Optional[str] = None,
    resume_data: Optional[ResumeData] = None,
) -> ResumeData:
    if user:
        if not resume_data:
            if not resume_name:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="If trying to generate resume form saved resumes, please provide the name or else provide data",
                )
            resume_data = get_resume(resume_name, user)

        if resume_data.personal_info.photo and not check_image_url(
            resume_data.personal_info.photo
        ):
            resume_data.personal_info.photo = user.photo_url

    else:
        if not resume_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Resume data not found"
            )
    return resume_data


async def create_resume(
    template: ResumeTemplateEnum,  # type: ignore
    output_type: ResumeOutputType,
    background_tasks: BackgroundTasks,
    resume_data: Annotated[ResumeData, Depends(resume_data)],
) -> FileResponseData:
    temp_resume: TempResume = await create_temp_resume_from_data(
        resume_data, template, output_type
    )
    background_tasks.add_task(shutil.rmtree, temp_resume.temp_dir)
    return prepare_file_response(temp_resume.path, "attachment")


async def tailored_resume_data(
    job_description: Annotated[str, Body()],
    resume_data: Annotated[ResumeData, Depends(resume_data)],
) -> ResumeData:
    return await tailor_resume(resume_data, job_description)


async def create_tailored_resume(
    template: ResumeTemplateEnum,  # type: ignore
    output_type: ResumeOutputType,
    background_tasks: BackgroundTasks,
    resume_data: Annotated[ResumeData, Depends(tailored_resume_data)],
) -> FileResponseData:
    temp_resume: TempResume = await create_temp_resume_from_data(
        resume_data, template, output_type
    )
    background_tasks.add_task(shutil.rmtree, temp_resume.temp_dir)
    return prepare_file_response(temp_resume.path, "attachment")
