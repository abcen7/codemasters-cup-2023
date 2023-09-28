from enum import Enum

WELCOME_MESSAGE = """
Привет 👋

👁️‍🗨️ Я Users Management Bot написанный @abcen7
⚒️ Я упрощаю управление информацией о сотрудниках.
⚡️ Я предоставляю удобный интерфейс для добавления, удаления, редактирования и поиска сотрудников.
"""

HELP_MESSAGE = """
Список моих команд
- /employee_add - создать карточку сотрудника
- /employee_update - обновить карточку сотрудника
- /employee_delete - удалить карточку сотрудника
- /employee_search - список команд поиска
"""


class UserRoles(Enum):
    USER = "user"
    ADMIN = "admin"


class UserRolesMessages(Enum):
    CHANGED = "✅ Роль была успешно изменена!"
    NOT_PERMITTED = "❌ У Вас недостаточно прав для использования этой команды!"


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
    PATRONYMIC = "patronymic"
    PERIOD_OF_TIME = "created"


class SearchResultMessages(Enum):
    SEARCH_RESULT_NOT_FOUND = "[🔎] Поиск не дал никакого ответа ..."


class EmployeeSearchMessages(Enum):
    SEARCH = """
    🔎 Давайте найдем сотрудника...
    Выберете, по какой характеристике его искать ниже
    """
    LIST_EMPLOYEES = "[👥] Список сотрудников:"
    LIST_JOB_TITLES = "[💼] Список должностей"
    WAITING = "[...] Бот уже ищет сотрудника!"
    ASK = "[💬] Введите данные: "
    ASK_PERIOD_OF_TIME = "[💬] Введите период времени (С какого по какое) в формате: \nГод-Месяц-Число-Часы-Минуты " \
                         "Год-Месяц-Число-Часы-Минуты \n" \
                         "Пример: 2023-09-28-23-00 2023-09-28-23-00"
    FAILED = "❌ Вы ввели данные в некорректном формате"
    LIST_COMMANDS = "[🔎] Бот умеет искать по 6 характеристикам: имя, фамилия, отчество, проект, должность, " \
                    "период прихода на работу"


class EmployeeKeysData(Enum):
    ID = '_id'
    AVATAR_PATH = 'avatar_path'
    CREATED = 'created'


DELETE_VERIFIED_YES = 'да'
NEW_LINE = "\n"

API_TO_RESULT = {
    'name': '<b>Имя</b>: ',
    'patronymic': '<b>Отчество</b>: ',
    'surname': '<b>Фамилия</b>: ',
    'job_title': '<b>Должность</b>: ',
    'project': '<b>Проект</b>: '
}
