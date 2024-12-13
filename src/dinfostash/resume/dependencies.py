import mimetypes
import os
import shutil
from typing import Optional

from fastapi import BackgroundTasks, Depends, HTTPException, status

from dinfostash.auth.dependencies import get_optional_current_user
from dinfostash.data.dependencies import get_resume
from dinfostash.data.models import ResumeData
from dinfostash.resume.constants import (
    FileResponseData,
    ResumeOutputType,
    ResumeTemplateEnum,
)
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


async def create_resume(
    template: ResumeTemplateEnum,
    output_type: ResumeOutputType,
    background_tasks: BackgroundTasks,
    user: Optional[User] = Depends(get_optional_current_user),
    resume_name: Optional[str] = None,
    resume_data: Optional[ResumeData] = None,
) -> FileResponseData:
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

    temp_resume = await create_temp_resume_from_data(resume_data, template, output_type)

    mime_type, _ = mimetypes.guess_type(temp_resume.path)
    media_type = mime_type or "application/octet-stream"
    headers = {"Content-Disposition": f'attachment; filename="{temp_resume.path}"'}
    # setting Content-Disposition as attachment ensures it is downloaded as a file

    background_tasks.add_task(shutil.rmtree, temp_resume.temp_dir)

    return FileResponseData(
        path=temp_resume.path, media_type=media_type, headers=headers
    )
