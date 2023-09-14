from fastapi import APIRouter, Depends, Form
from starlette import status
from typing import Annotated

from .services import UsersService
from .models import User

users_router = APIRouter()


@users_router.post("/users",
                   status_code=status.HTTP_201_CREATED,
                   response_model=User)
async def create_user(
        user: User,
        users_service: UsersService = Depends(),
) -> User:
    return await users_service.create(user.dict(exclude_unset=True))
