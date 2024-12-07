from requests import HTTPError
from fastapi import HTTPException, status

def raise_detailed_error(request_object):
    try:
        request_object.raise_for_status()
    except HTTPError as e:
        # raise detailed error message
        # TODO: Check if we get a { "error" : "Permission denied." } and handle automatically
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
