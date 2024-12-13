import mimetypes
import os
import shutil
from typing import Annotated

from fastapi import BackgroundTasks, Depends

from dinfostash.auth.dependencies import get_current_user
from dinfostash.data.dependencies import get_resume
from dinfostash.data.models import ResumeData
from dinfostash.resume.constants import (FileResponseData, ResumeOutputType,
                                         ResumeTemplateEnum)
from dinfostash.resume.services import create_temp_resume_from_data
from dinfostash.resume.utils import check_image_url
from dinfostash.user.models import User


async def template_preview(
    template: ResumeTemplateEnum,
    output_type: ResumeOutputType,
) -> FileResponseData:

    files = [
        f
        for f in os.listdir("example/outputs")
        if f.endswith(output_type.value) and template.value in f
    ]

    first_file_path = f"example/outputs/{files[0]}"

    mime_type, _ = mimetypes.guess_type(first_file_path)
    media_type = mime_type or "application/octet-stream"
    headers = {"Content-Disposition": f'inline; filename="{first_file_path}"'}
    # setting Content-Disposition as inline ensures it is displayed in browser

    return FileResponseData(
        path=first_file_path, media_type=media_type, headers=headers
    )


async def create_resume_from_saved_data(
    template: ResumeTemplateEnum,
    output_type: ResumeOutputType,
    resume_data: Annotated[ResumeData, Depends(get_resume)],
    user: Annotated[User, Depends(get_current_user)],
    background_tasks: BackgroundTasks,
) -> FileResponseData:

    if resume_data.personal_info.photo and not check_image_url(
        resume_data.personal_info.photo
    ):
        resume_data.personal_info.photo = user.photo_url

    temp_resume = await create_temp_resume_from_data(resume_data, template, output_type)

    mime_type, _ = mimetypes.guess_type(temp_resume.path)
    media_type = mime_type or "application/octet-stream"
    headers = {"Content-Disposition": f'attachment; filename="{temp_resume.path}"'}
    # setting Content-Disposition as attachment ensures it is downloaded as a file

    background_tasks.add_task(shutil.rmtree, temp_resume.temp_dir)

    return FileResponseData(
        path=temp_resume.path, media_type=media_type, headers=headers
    )


async def create_resume_from_data(
    template: ResumeTemplateEnum,
    output_type: ResumeOutputType,
    resume_data: ResumeData,
    background_tasks: BackgroundTasks,
) -> FileResponseData:

    temp_resume = await create_temp_resume_from_data(resume_data, template, output_type)

    mime_type, _ = mimetypes.guess_type(temp_resume.path)
    media_type = mime_type or "application/octet-stream"
    headers = {"Content-Disposition": f'attachment; filename="{temp_resume.path}"'}
    # setting Content-Disposition as attachment ensures it is downloaded as a file

    background_tasks.add_task(shutil.rmtree, temp_resume.temp_dir)

    return FileResponseData(
        path=temp_resume.path, media_type=media_type, headers=headers
    )
