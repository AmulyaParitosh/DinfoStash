from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

import pytest

from src.resumegenerator.cli_app import generate_resume
from src.resumegenerator.resume import ResumeTemplate


def test_generate_resume_valid_args():
    # Mock the Namespace object that argparse would usually provide to your function
    args = Namespace(
        datafile_path=Path("example/inputs/example_resume_data.json"),
        output_path=Path("example/outputs/single_column_photo"),
        template=ResumeTemplate.SINGLE_COLUMN_PHOTO,
    )

    # Use the patch function to mock the create_resume function
    # This allows us to test generate_resume in isolation
    with patch("src.resumegenerator.resume.create_resume") as mock_create_resume:
        generate_resume(args)

    # Check that create_resume was called with the correct arguments
    mock_create_resume.assert_called_once_with(
        args.datafile_path,
        args.output_path,
        args.template,
    )


def test_generate_resume_invalid_args():
    # Mock the Namespace object with an invalid datafile_path
    args = Namespace(
        datafile_path=Path("example/inputs/non_existent_file.json"),
        output_path=Path("example/outputs/single_column_photo"),
        template=ResumeTemplate.SINGLE_COLUMN_PHOTO,
    )

    # Use the patch function to mock the create_resume function
    # This allows us to test generate_resume in isolation
    with patch("src.resumegenerator.resume.create_resume") as mock_create_resume:
        # Since the datafile_path is invalid, we expect create_resume to raise an Exception
        with pytest.raises(Exception):
            generate_resume(args)

    # Check that create_resume was called with the correct arguments
    mock_create_resume.assert_called_once_with(
        args.datafile_path,
        args.output_path,
        args.template,
    )
