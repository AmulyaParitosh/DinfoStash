import json
import random
from pathlib import Path

import pytest
from faker import Faker

from ResumeGenerator.src.data import (
    Achievement,
    Address,
    ContactInfo,
    Education,
    Experience,
    Marks,
    PersonalInfo,
    Project,
    ResumeData,
    Skill,
)

fake = Faker()


# Generate ContactInfo
def fake_contact_info():
    return ContactInfo(
        type=fake.word(),
        display=fake.word(),
        link=fake.url(),
        fa_icon=fake.word(),
    )


# Generate Address
def fake_address():
    return Address(
        line1=fake.street_address(),
        line2=fake.secondary_address(),
        city=fake.city(),
        state=fake.state(),
        country=fake.country(),
        pin_code=fake.random_int(min=10000, max=99999),
    )


# Generate PersonalInfo
def fake_personal_info():
    return PersonalInfo(
        name=fake.name(),
        photo="ResumeGenerator/example/inputs/john_doe.jpeg",
        address=fake_address(),
        contact_infos=[fake_contact_info() for _ in range(random.randint(1, 3))],
    )


# Generate Marks
def fake_marks():
    return Marks(
        type=fake.word(),
        value=fake.random_number(digits=2),
    )


# Generate Education
def fake_education():
    return Education(
        institute=fake.word(),
        degree=fake.word(),
        status=fake.word(),
        year=fake.year(),
        marks=fake_marks(),
    )


# Generate Skill
def fake_skill():
    return Skill(
        type=fake.word(),
        values=[fake.word() for _ in range(random.randint(1, 3))],
    )


# Generate Experience
def fake_experience():
    return Experience(
        organization=fake.company(),
        position=fake.job(),
        date=fake.date(),
        link=fake.url(),
        descriptions=[fake.sentence() for _ in range(random.randint(1, 3))],
        technologies=[fake.word() for _ in range(random.randint(1, 3))],
    )


# Generate Project
def fake_project():
    return Project(
        name=fake.word(),
        link=fake.url(),
        technologies=[fake.word() for _ in range(random.randint(1, 3))],
        description=fake.sentence(),
    )


# Generate Achievement
def fake_achievement():
    return Achievement(
        type=fake.word(),
        title=fake.sentence(),
        data=fake.sentence(),
    )


def test_contact_info():
    contact_info = fake_contact_info()
    assert isinstance(contact_info, ContactInfo)


def test_address():
    address = fake_address()
    assert isinstance(address, Address)


def test_personal_info():
    personal_info = fake_personal_info()
    assert isinstance(personal_info, PersonalInfo)


def test_marks():
    marks = fake_marks()
    assert isinstance(marks, Marks)


def test_education():
    education = fake_education()
    assert isinstance(education, Education)


def test_skill():
    skill = fake_skill()
    assert isinstance(skill, Skill)


def test_experience():
    experience = fake_experience()
    assert isinstance(experience, Experience)


def test_project():
    project = fake_project()
    assert isinstance(project, Project)


def test_achievement():
    achievement = fake_achievement()
    assert isinstance(achievement, Achievement)


def test_resume_data():
    resume_data = ResumeData(
        personal_info=fake_personal_info(),
        educations=[fake_education() for _ in range(3)],
        skills=[fake_skill() for _ in range(3)],
        experience=[fake_experience() for _ in range(3)],
        projects=[fake_project() for _ in range(3)],
        achievements=[fake_achievement() for _ in range(3)],
    )
    assert isinstance(resume_data, ResumeData)


# Test for invalid photo path
def test_invalid_photo_path():
    with pytest.raises(ValueError):
        PersonalInfo(
            name=fake.name(),
            photo=fake.file_path(),
            address=fake_address(),
            contact_infos=[fake_contact_info() for _ in range(random.randint(1, 3))],
        )


def test_load_data():
    # Write the fake data to a temporary JSON file
    resume_data = ResumeData(
        personal_info=fake_personal_info(),
        educations=[fake_education() for _ in range(3)],
        skills=[fake_skill() for _ in range(3)],
        experience=[fake_experience() for _ in range(3)],
        projects=[fake_project() for _ in range(3)],
        achievements=[fake_achievement() for _ in range(3)],
    )
    path = Path("temp.json")
    with path.open("w", encoding="utf-8") as json_file:
        json.dump(resume_data.model_dump(), json_file, indent=4)

    # Load the data from the file
    loaded_data = ResumeData.read_from_file(path)
    assert isinstance(loaded_data, ResumeData)

    # Clean up the temporary file
    path.unlink()
