from aiogram.types import \
    InlineKeyboardButton, \
    InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, \
    KeyboardButton

from aiogram.utils.callback_data import CallbackData

from handlers.constants import UserSearchMessages
from keyboards.constants import \
    COMMANDS_MESSAGE, \
    EMPLOYEE_ADD_TEXT, \
    EMPLOYEE_DELETE_TEXT, \
    EMPLOYEE_SEARCH_TEXT, \
    OPTIONAL_FIELD, \
    STOP_FILLING, EMPLOYEE_UPDATE_TEXT, EMPLOYEE_UPDATE_DATA, DONT_UPDATE_FIELD

from keyboards.constants import \
    EMPLOYEE_ADD_DATA, \
    EMPLOYEE_REMOVE_DATA, \
    EMPLOYEE_SEARCH_DATA

executor_cb = CallbackData("executor", "action")


def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(COMMANDS_MESSAGE)
    )


def get_commands_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=EMPLOYEE_ADD_TEXT,
                    callback_data=executor_cb.new(
                        action=EMPLOYEE_ADD_DATA
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text=EMPLOYEE_UPDATE_TEXT,
                    callback_data=executor_cb.new(
                        action=EMPLOYEE_UPDATE_DATA
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text=EMPLOYEE_DELETE_TEXT,
                    callback_data=executor_cb.new(
                        action=EMPLOYEE_REMOVE_DATA
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text=EMPLOYEE_SEARCH_TEXT,
                    callback_data=executor_cb.new(
                        action=EMPLOYEE_SEARCH_DATA
                    ),
                )
            ],
        ],
    )


def get_optional_and_dont_update_keyboard() -> InlineKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(OPTIONAL_FIELD)
    ).add(
        KeyboardButton(DONT_UPDATE_FIELD)
    )


def get_optional_field_keyboard() -> InlineKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(OPTIONAL_FIELD)
    )


def get_dont_update_field_keyboard() -> InlineKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(DONT_UPDATE_FIELD)
    )


def get_stop_filling_keyboard() -> InlineKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(STOP_FILLING)
    )


def get_search_keyboard() -> InlineKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(UserSearchKeyboardTypes.USER_SEARCH_NAME.value),
        KeyboardButton(UserSearchKeyboardTypes.USER_SEARCH_SURNAME.value),
        KeyboardButton(UserSearchKeyboardTypes.USER_SEARCH_PROJECT.value),
        KeyboardButton(UserSearchKeyboardTypes.USER_SEARCH_JOB_TITLE.value),
        KeyboardButton(UserSearchKeyboardTypes.USER_SEARCH_UNION_SEARCH.value),
    )
