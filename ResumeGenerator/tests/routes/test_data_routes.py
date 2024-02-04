from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ResumeGenerator.api import app
from ResumeGenerator.src.data import ResumeData

client = TestClient(app)


expected_data = ResumeData.load_data(
    Path(
        "/home/encryptedbee/tesla/projects/ResumeGenerator/ResumeGenerator/example/inputs/example_resume_data.json"
    )
).model_dump()


def test_read_resume():
    response = client.get("/resume/data")
    assert response.status_code == 200
    assert response.json() == expected_data


def test_read_personal_info():
    response = client.get("/resume/data/personal_info")
    assert response.status_code == 200
    print(f"{response.json()=}")
    assert response.json() == expected_data["personal_info"]


def test_read_contact_infos():
    response = client.get("/resume/data/personal_info/contact_infos")
    assert response.status_code == 200
    assert response.json() == expected_data["personal_info"]["contact_infos"]


def test_read_educations():
    response = client.get("/resume/data/educations")
    assert response.status_code == 200
    assert response.json() == expected_data["educations"]


def test_read_skills():
    response = client.get("/resume/data/skills")
    assert response.status_code == 200
    assert response.json() == expected_data["skills"]


def test_read_experience():
    response = client.get("/resume/data/experience")
    assert response.status_code == 200
    assert response.json() == expected_data["experience"]


def test_read_projects():
    response = client.get("/resume/data/projects")
    assert response.status_code == 200
    assert response.json() == expected_data["projects"]


def test_read_achievements():
    response = client.get("/resume/data/achievements")
    assert response.status_code == 200
    assert response.json() == expected_data["achievements"]
