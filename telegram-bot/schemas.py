from typing import List, Literal, Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    categories: Optional[List[str]]


class TelegramMessage(BaseModel):
    telegram_id: int
    message: str


class BroadcastRequest(BaseModel):
    messages: List[TelegramMessage]
    type: Optional[Literal["executor", "customer"]]
    order_id: Optional[int]
    parse_mode: Optional[Literal["HTML", "MarkdownV2", "Markdown"]]
