from fastapi import HTTPException, status


class TooLargeFile(HTTPException):
    def __init__(self, file_size: int) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The file has too much weight. Permissible weight - 30 MB. File weight - {file_size}",
        )


class InvalidFilename(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filename"
        )