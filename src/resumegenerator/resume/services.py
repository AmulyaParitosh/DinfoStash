import tempfile
from pathlib import Path

from ..data.models import ResumeData
from .constants import ResumeOutputType, ResumeTemplateEnum, TempResume
from .resume_templates import ResumeTemplate
from .utils import download_img


def create_resume_from_file(
    datafile_path: Path, outputdir_path: Path, resume_template: ResumeTemplateEnum
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
    data: ResumeData, resume_template: ResumeTemplateEnum, output_type: ResumeOutputType
):
    temp_dir = tempfile.mkdtemp()

    if img_url := data.personal_info.photo:
        data.personal_info.photo = f"{temp_dir}/photo.jpg"
        download_img(img_url, data.personal_info.photo)

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
