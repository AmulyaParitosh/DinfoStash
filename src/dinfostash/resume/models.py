from pydantic import BaseModel


class ResumeTemplateMetadata(BaseModel):
    display_name: str
    details: str
    number_format_columns: int
    includes_photo: bool
    headings: list[str]
