from pathlib import Path


def file_exists(value: str):
    file_path = Path(value)
    if not file_path.exists():
        raise ValueError(f"File {file_path} does not exist")
    return str(file_path.absolute())
