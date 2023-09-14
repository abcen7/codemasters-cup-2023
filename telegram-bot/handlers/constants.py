from enum import Enum, auto

WELCOME_MESSAGE = """
Привет 👋

👁️‍🗨️ Я Users Management Bot написанный @abcen7
⚒️ Я упрощаю управление информацией о сотрудниках.
⚡️ Я предоставляю удобный интерфейс для добавления, удаления, редактирования и поиска сотрудников.
"""

HELP_MESSAGE = """
Список моих команд
- /user_add
- /user_remove
- /user_search
"""


class EmployeeAskDataMessages(Enum):
    ID = "💬 Введите уникальный идентификатор сотрудника"
    NAME = "💬 Введите имя"
    SURNAME = "💬 Введите фамилию"
    PATRONYMIC = "💬 Введите отчество (Опционально)"
    JOB_TITLE = "💬 Введите должность"
    PROJECT = "💬 Введите проект сотрудника"
    AVATAR = "💬 Прикрепите аватарку сотрудника (Опционально)"


class EmployeeCreateMessages(Enum):
    CREATE = "🪪 Давайте заполним карточку нового сотрудника!"
    CANCEL = "❌ Вы отменили создание карточки нового сотрудника"
    SUCCESS = "✅ Отлично! Вы успешно создали карточку сотрудника!"
    STOPPED = "❌ Заполнение прервано. Все данные сброшены."


class EmployeeUpdateMessages(Enum):
    INVALID_ID = "❌ Вы ввели некорректный ID, или такого не сотрудника не существует"
    UPDATE = "🪪 Давайте обновим карточку сотрудника!"
    CANCEL = "❌ Вы отменили обновление карточки сотрудника"
    SUCCESS = "✅ Отлично! Вы успешно обновили карточку сотрудника!"
    STOPPED = "❌ Заполнение прервано. Все данные сброшены."


class EmployeeDeleteMessages(Enum):
    INVALID_ID = "❌ Вы ввели некорректный ID, или такого не сотрудника не существует"
    DELETE = "🪪 Давайте удалим карточку сотрудника!"
    CANCEL = "❌ Вы отменили удаление карточки сотрудника"
    SUCCESS = "✅ Отлично! Вы успешно удалили карточку сотрудника!"
    IS_VERIFIED = "[⁉️] Вы уверены, что хотите удалить карточку сотрудника. Напишите [да] или [нет]"


class SearchType(Enum):
    NAME = "name"
    SURNAME = "surname"
    PROJECT = "project"
    JOB_TITLE = "job_title"


class SearchResultMessages(Enum):
    SEARCH_RESULT_NOT_FOUND = "[🔎] Поиск не дал никакого ответа ..."


class UserSearchMessages(Enum):
    USER_SEARCH_MESSAGE = """
    🔎 Давайте найдем пользователя...
    Выберете, по какой характеристике его искать ниже
    """
    USER_SEARCH_WAITING = "Бот уже ищет сотрудника!"
    USER_SEARCH_ASK = "[💬] Введите данные: "
    LIST_SEARCH_COMMANDS = """
    [🔎] Бот умеет искать по 4 характеристикам: имя, фамилия, проект, позиция на работе:
    - /search_employee_name
    - /search_employee_surname
    - /search_employee_job_title
    - /search_employee_project
    """


API_TO_RESULT = {
    'name': '<b>Имя</b>: ',
    'patronymic': '<b>Отчество</b>: ',
    'surname': '<b>Фамилия</b>: ',
    'job_title': '<b>Должность</b>: ',
    'project': '<b>Проект</b>: '
}

NEW_LINE = "\n"
AVATAR_PATH = 'avatar_path'
CREATED = 'created'
ID = '_id'
