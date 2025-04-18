from pathlib import Path

import pytest

from src.dinfostash.resume import ResumeTemplate, create_resume_from_file


def test_create_resume_single_column_photo():
    # Set the paths
    data_path = Path("example/inputs/example_resume_data.json")
    output_path = Path("example/outputs")
    resume_format = ResumeTemplate.SINGLE_COLUMN_PHOTO

    # Create the resume
    create_resume_from_file(data_path, output_path, resume_format)

    # Check that the output file exists
    output_path = output_path / "John_Doe_SINGLE_COLUMN_PHOTO.pdf"
    assert output_path.exists()


def test_create_resume_single_column_nophoto():
    # Set the paths
    data_path = Path("example/inputs/example_resume_data.json")
    output_path = Path("example/outputs/")
    resume_format = ResumeTemplate.SINGLE_COLUMN_NOPHOTO

    # Create the resume
    create_resume_from_file(data_path, output_path, resume_format)
    output_path = output_path / "John_Doe_SINGLE_COLUMN_NOPHOTO.pdf"

    # Check that the output file exists
    assert output_path.exists()


def test_create_resume_empty_json():
    # Set the paths
    data_path = Path("example/inputs/empty.json")
    output_path = Path("example/outputs")
    resume_format = ResumeTemplate.SINGLE_COLUMN_PHOTO

    # Create the resume
    with pytest.raises(Exception):
        create_resume_from_file(data_path, output_path, resume_format)


def test_create_resume_invalid_path():
    # Set the paths
    data_path = Path("example/inputs/non_existent_file.json")
    output_path = Path("example/outputs")
    resume_format = ResumeTemplate.SINGLE_COLUMN_PHOTO

    # Create the resume
    with pytest.raises(Exception):
        create_resume_from_file(data_path, output_path, resume_format)
