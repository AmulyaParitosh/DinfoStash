from pathlib import Path

from ..src.dinfostash.resume import create_resume_from_file


if __name__ == "__main__":
    create_resume_from_file(
        Path("example/inputs/example_resume_data.json"),
        Path("example/outputs/example_resume"),
        "SingleColumnNoPhoto",
    )
    print("Resume generated successfully.")
