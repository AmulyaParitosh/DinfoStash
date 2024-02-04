import json
from pathlib import Path
from typing import List, Optional, Union

from pydantic import AnyUrl, BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class ContactInfo(BaseModel):
    type: str
    display: str
    link: Union[AnyUrl, EmailStr, PhoneNumber]
    fa_icon: str


class Address(BaseModel):
    line1: str
    line2: Optional[str] = ""
    city: str
    state: str
    country: str
    pin_code: int


class PersonalInfo(BaseModel):
    name: str
    photo: Path
    address: Address
    contact_infos: List[ContactInfo]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.photo = self.photo.absolute()


class Marks(BaseModel):
    type: str
    value: float


class Education(BaseModel):
    institute: str
    degree: str
    status: str
    year: int
    marks: Marks


class Skill(BaseModel):
    type: str
    values: List[str]


class Experience(BaseModel):
    organization: str
    position: str
    date: str
    link: Optional[AnyUrl] = ""
    descriptions: List[str]
    technologies: List[str]


class Project(BaseModel):
    name: str
    link: Optional[AnyUrl] = ""
    technologies: List[str]
    description: str


class Achievement(BaseModel):
    type: str
    title: str
    data: str


class ResumeData(BaseModel):
    personal_info: PersonalInfo
    educations: List[Education]
    skills: List[Skill]
    experience: List[Experience]
    projects: List[Project]
    achievements: List[Achievement]


def load_data(path: Path) -> ResumeData:
    with path.open("r", encoding="utf-8") as json_file:
        json_str = json_file.read().replace("#", r"\\#")
        json_data: dict = json.loads(json_str)
        return ResumeData(**json_data)


if __name__ == "__main__":
    obj = load_data(Path("resume_data.json"))
    print(obj)
    print(type(obj))
    print(type(obj.skills))
    print(obj.skills[0])
