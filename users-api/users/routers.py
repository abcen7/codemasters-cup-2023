from fastapi import APIRouter, Depends, Form
from starlette import status
from typing import Annotated

from .schemas import UpdateUser
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
    return await users_service.create(user)


@users_router.patch("/users/{telegram_id}",
                    status_code=status.HTTP_200_OK,
                    response_model=User)
async def update_user(
        telegram_id: int,
        params_for_update: UpdateUser,
        users_service: UsersService = Depends(),
) -> User:
    return await users_service.update(telegram_id, params_for_update)


@users_router.get("/users/{telegram_id}",
                  status_code=status.HTTP_200_OK,
                  response_model=User)
async def get_user(
        telegram_id: int,
        users_service: UsersService = Depends(),
) -> User:
    return await users_service.get_one(telegram_id)
