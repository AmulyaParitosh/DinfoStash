from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from .constants import AnyUrlStr, ImagePath

# TODO: the base model uses = Filed(...) to define required fields, ise annotated with its datatype as it is creating issue with type hinting


class ContactInfo(BaseModel):
    type: str = Field(
        ...,
        title="Contact Type",
        description="Type of contact information (e.g., email, phone)",
        min_length=3,
        max_length=50,
    )
    display: str = Field(
        ...,
        title="Display Name",
        description="Display name for the contact information",
        min_length=3,
        max_length=100,
    )
    link: Union[AnyUrlStr, EmailStr, PhoneNumber] = Field(
        ..., title="Contact Link", description="Link to the contact information"
    )
    fa_icon: str = Field(
        ...,
        title="Font Awesome Icon",
        description="Font Awesome icon name",
        min_length=3,
        max_length=50,
    )


class Address(BaseModel):
    line1: str = Field(
        ...,
        title="Address Line 1",
        description="First line of the address",
        min_length=1,
        max_length=100,
    )
    line2: Optional[str] = Field(
        "",
        title="Address Line 2",
        description="Second line of the address, if any",
        max_length=100,
    )
    city: str = Field(
        ...,
        title="City",
        description="City of the address",
        min_length=1,
        max_length=50,
    )
    state: str = Field(
        ...,
        title="State",
        description="State of the address",
        min_length=1,
        max_length=50,
    )
    country: str = Field(
        ...,
        title="Country",
        description="Country of the address",
        min_length=1,
        max_length=50,
    )
    pin_code: int = Field(
        ...,
        title="Postal Code",
        description="Postal code of the address",
        ge=100000,
        le=999999,
    )


class PersonalInfo(BaseModel):
    name: str = Field(
        ...,
        title="Name",
        description="Name of the person",
        min_length=1,
        max_length=100,
    )
    photo: Optional[ImagePath] = Field(
        ..., title="Photo", description="Absolute file path to the photo"
    )
    address: Address = Field(..., title="Address", description="Address information")
    contact_infos: List[ContactInfo] = Field(
        ..., title="Contact Information", description="List of contact information"
    )
    short_infos: List[str] = Field(
        ..., title="Short Information", description="List of short information snippets"
    )

    @field_validator("short_infos")
    @classmethod
    def validate_short_infos(cls, v):
        if len(v) == 0:
            raise ValueError("short_infos must have at least one item")
        return v


class Marks(BaseModel):
    type: str = Field(
        ...,
        title="Marks Type",
        description="Type of marks (e.g., percentage, GPA)",
        min_length=1,
        max_length=20,
    )
    value: float = Field(
        ..., title="Marks Value", description="Value of the marks", gt=0, le=100
    )


class Education(BaseModel):
    institute: str = Field(
        ...,
        title="Institute",
        description="Name of the educational institute",
        min_length=1,
        max_length=100,
    )
    degree: str = Field(
        ...,
        title="Degree",
        description="Degree obtained or being pursued",
        min_length=1,
        max_length=100,
    )
    status: str = Field(
        ...,
        title="Status",
        description="Current status of the education (e.g., completed, ongoing)",
        max_length=20,
    )
    year: int = Field(
        ...,
        title="Year",
        description="Year of graduation or expected graduation",
        ge=1900,
        le=2100,
    )
    marks: Marks = Field(
        ..., title="Marks", description="Marks obtained in the education"
    )


class Skill(BaseModel):
    type: str = Field(
        ...,
        title="Skill Type",
        description="Type of skill (e.g., technical, soft)",
        min_length=1,
        max_length=50,
    )
    values: List[str] = Field(
        ..., title="Skill Values", description="List of specific skills"
    )

    @field_validator("values")
    @classmethod
    def validate_values(cls, v):
        if len(v) == 0:
            raise ValueError("values must have at least one item")
        return v


class Experience(BaseModel):
    organization: str = Field(
        ...,
        title="Organization",
        description="Name of the organization",
        min_length=1,
        max_length=100,
    )
    position: str = Field(
        ...,
        title="Position",
        description="Position held at the organization",
        min_length=1,
        max_length=100,
    )
    date: str = Field(
        ...,
        title="Date",
        description="Date or duration of the experience",
        min_length=1,
        max_length=50,
    )
    link: Optional[AnyUrlStr] = Field(
        None, title="Link", description="Link to the organization or project"
    )
    location: Optional[str] = Field(
        None, title="Location", description="Location of the experience", max_length=100
    )
    descriptions: List[str] = Field(
        ...,
        title="Descriptions",
        description="List of descriptions of the role and responsibilities",
    )
    technologies: List[str] = Field(
        ..., title="Technologies", description="List of technologies used"
    )

    @field_validator("descriptions", "technologies")
    @classmethod
    def validate_lists(cls, v):
        if len(v) == 0:
            raise ValueError("must have at least one item")
        return v


class Project(BaseModel):
    name: str = Field(
        ...,
        title="Project Name",
        description="Name of the project",
        min_length=1,
        max_length=100,
    )
    link: Optional[AnyUrlStr] = Field(
        None, title="Project Link", description="Link to the project"
    )
    type: Optional[str] = Field(
        None,
        title="Project Type",
        description="Type of project",
        max_length=50,
    )
    organization: Optional[str] = Field(
        None,
        title="Organization",
        description="Organization under which the project was done",
        max_length=100,
    )
    time: Optional[str] = Field(
        None,
        title="Time Period",
        description="Time period of the project",
        max_length=50,
    )
    technologies: List[str] = Field(
        ...,
        title="Technologies",
        description="List of technologies used in the project",
    )
    description: str = Field(
        ..., title="Description", description="Description of the project", min_length=1
    )

    @field_validator("technologies")
    @classmethod
    def validate_project_technologies(cls, v):
        if len(v) == 0:
            raise ValueError("technologies must have at least one item")
        return v


class Achievement(BaseModel):
    type: str = Field(
        ...,
        title="Achievement Type",
        description="Type of achievement",
        min_length=1,
        max_length=50,
    )
    title: str = Field(
        ...,
        title="Title",
        description="Title of the achievement",
        min_length=1,
        max_length=100,
    )
    data: str = Field(
        ...,
        title="Data",
        description="Detailed information about the achievement",
        min_length=1,
    )
    link: Optional[AnyUrlStr] = Field(
        None,
        title="Achievement Link",
        description="Link to the Achievement for validation",
    )


class ResumeData(BaseModel):
    personal_info: PersonalInfo = Field(
        ...,
        title="Personal Information",
        description="Personal information of the individual",
    )
    educations: List[Education] = Field(
        ..., title="Educations", description="List of educational qualifications"
    )
    skills: List[Skill] = Field(..., title="Skills", description="List of skills")
    experience: List[Experience] = Field(
        ..., title="Experience", description="List of work experiences"
    )
    projects: List[Project] = Field(
        ..., title="Projects", description="List of projects"
    )
    achievements: List[Achievement] = Field(
        ..., title="Achievements", description="List of achievements"
    )

    @field_validator("educations", "skills", "experience", "projects", "achievements")
    @classmethod
    def validate_lists(cls, v):
        if len(v) == 0:
            raise ValueError("must have at least one item")
        return v

    @staticmethod
    def read_from_file(path: Path) -> ResumeData:
        with path.open("r", encoding="utf-8") as json_file:
            json_data: dict = json.load(json_file)
            return ResumeData(**json_data)

    def data_for_latex(self) -> ResumeData:
        LATEX_ESCAPE_CHARS = ["#", "%", "&"]
        json_str = self.model_dump_json()
        for char in LATEX_ESCAPE_CHARS:
            json_str = json_str.replace(char, rf"\\{char}")
        return ResumeData(**json.loads(json_str))


# with open("json_schema.json", "w") as f:
#     json.dump(ResumeData.model_json_schema(), f, indent=2)
