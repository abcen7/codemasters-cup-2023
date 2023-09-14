import hashlib
import hmac
from urllib.parse import unquote
from .exceptions import InvalidTgData
from ..config import TELEGRAM_BOT_TOKEN


class ValidationTelegramData:
    keygen = [
        lambda token: hashlib.sha256(token).digest(),
        lambda token: hmac.new("WebAppData".encode(),
                               token, hashlib.sha256).digest()
    ]

    @staticmethod
    def validate(telegram_data: str, telegram_id: int) -> bool:
        # if not ValidationTelegramData._comparison(telegram_data, telegram_id):
        #    raise InvalidTgData
        return True

    @staticmethod
    def _comparison(telegram_data: str, telegram_id: int) -> bool:
        data_check_string, valid_hash = ValidationTelegramData._get_check_string(
            telegram_data, telegram_id)
        telegram_bot_token: bytes = TELEGRAM_BOT_TOKEN.encode()
        secret_key: bytes = ValidationTelegramData.keygen["query_id" in telegram_data or "chat_instance" in telegram_data](
            telegram_bot_token)
        calculated_hash: str = hmac.new(
            secret_key,
            data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        return calculated_hash == valid_hash

    @staticmethod
    def _get_check_string(telegram_data: str, telegram_id: int) -> bool:
        if str(telegram_id) not in telegram_data:
            raise InvalidTgData

        init_data = sorted([chunk.split("=")
                            for chunk in unquote(telegram_data).split("&")
                            if not (chunk[:5] == "hash=" and (valid_hash := chunk[5:]))],
                           key=lambda x: x[0])

        return "\n".join([f"{rec[0]}={rec[1]}" for rec in init_data]), valid_hash
