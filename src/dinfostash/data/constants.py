from typing import Annotated

from pydantic import AnyUrl, BeforeValidator, TypeAdapter

from ..firebase import users_collection
from .utils import file_exists

AnyUrlTypeAdapter = TypeAdapter(AnyUrl)
AnyUrlStr = Annotated[
    str,
    BeforeValidator(
        lambda value: (
            (AnyUrlTypeAdapter.validate_python(value) and value) if value else ""
        )
    ),
]

AbsoluteFilePath = Annotated[
    str,
    BeforeValidator(file_exists),
]

ImagePath = AnyUrlStr | AbsoluteFilePath
