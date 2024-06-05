from enum import Enum
from typing import NamedTuple

from .resume_templates import Resume


class ResumeOutputType(Enum):
    PDF = "pdf"
    TEX = "tex"


FileResponseData = NamedTuple(
    "FileResponseData",
    [("path", str), ("media_type", str), ("headers", dict)],
)

TempResume = NamedTuple(
    "TempResume",
    [("path", str), ("temp_dir", str)],
)

ResumeTemplateEnum = Enum(
    "ResumeTemplateEnum", {k: k for k in Resume.available_templates()}
)
