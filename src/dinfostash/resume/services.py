import tempfile
from pathlib import Path
import mimetypes
from typing import Literal
from fastapi import HTTPException, status
from dinfostash.data.models import ResumeData
from dinfostash.resume.constants import (
    ResumeOutputType,
    ResumeTemplateEnum,
    TempResume,
    FileResponseData,
)
from dinfostash.resume.resume_templates import ResumeTemplate
from dinfostash.resume.utils import download_img


def create_resume_from_file(
    datafile_path: Path, outputdir_path: Path, resume_template: ResumeTemplateEnum  # type: ignore
):

    data_obj = ResumeData.read_from_file(datafile_path)
    latex_data_obj = data_obj.data_for_latex()

    latex_resume = ResumeTemplate.get_template_by_name(
        resume_template.value
    ).create_document(latex_data_obj)

    output_path = (
        outputdir_path
        / f"{data_obj.personal_info.name.replace(' ', '_')}_{resume_template.value}"
    )

    latex_resume.generate_pdf(str(output_path))
    latex_resume.generate_tex(str(output_path))


async def create_temp_resume_from_data(
    data: ResumeData, resume_template: ResumeTemplateEnum, output_type: ResumeOutputType  # type: ignore
):
    temp_dir = tempfile.mkdtemp()

    if img_url := data.personal_info.photo:
        data.personal_info.photo = f"{temp_dir}/photo.jpg"
        try:
            download_img(img_url, data.personal_info.photo)
        except ValueError as exp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid Image URL for profile pic",
            )

    output_path = f"{temp_dir}/{data.personal_info.name.replace(' ', '_')}_{resume_template.value}"

    latex_data_obj = data.data_for_latex()
    latex_resume = ResumeTemplate.get_template_by_name(
        resume_template.value
    ).create_document(latex_data_obj)

    if output_type == ResumeOutputType.PDF:
        latex_resume.generate_pdf(
            str(output_path), compiler="pdflatex", compiler_args=["--shell-escape"]
        )
    elif output_type == ResumeOutputType.TEX:
        latex_resume.generate_tex(str(output_path))

    return TempResume(path=f"{output_path}.{output_type.value}", temp_dir=temp_dir)


def prepare_file_response(
    file_path: str,
    content_disposition: Literal["inline"] | Literal["attachment"],
) -> FileResponseData:
    mime_type, _ = mimetypes.guess_type(file_path)
    media_type = mime_type or "application/octet-stream"
    # setting Content-Disposition as attachment ensures it is downloaded as a file
    headers = {"Content-Disposition": f'{content_disposition}; filename="{file_path}"'}

    return FileResponseData(path=file_path, media_type=media_type, headers=headers)
