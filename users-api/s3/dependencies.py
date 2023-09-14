import uuid
from .exceptions import InvalidFilename


def is_valid_filename(filename: str):
    try:
        uuid.UUID(str(filename))
        return filename
    except ValueError:
        raise InvalidFilename