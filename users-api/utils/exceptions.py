from fastapi import HTTPException, status


class InvalidTgData(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid telegram data",
        )
