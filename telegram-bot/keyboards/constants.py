from enum import Enum

COMMANDS_MESSAGE = "🔑 Команды"


class EmployeeMainButtons(Enum):
    ADD_TEXT = "🆕 Создать карточку сотрудника"
    UPDATE_TEXT = "✍️ Обновить карточку сотрудника"
    DELETE_TEXT = "❌️ Удалить карточку сотрудника"
    SEARCH_TEXT = "👀 Найти карточку сотрудника"
    ADD_DATA = "employee_add"
    UPDATE_DATA = "employee_update"
    DELETE_DATA = "employee_remove"
    SEARCH_DATA = "employee_search"


class EmployeeSearchButtons(Enum):
    NAME_TEXT = "[🔎] Поиск по имени"
    SURNAME_TEXT = "[🔎] Поиск по фамилии"
    PROJECT_TEXT = "[🔎] Поиск по проекту"
    JOB_TITLE_TEXT = "[🔎] Поиск по должности"
    PATRONYMIC_TEXT = "[🔎] Поиск по отчеству"
    PERIOD_OF_TIME_TEXT = "[🔎] Поиск по периоду времени"
    NAME_DATA = "employee_search_name"
    SURNAME_DATA = "employee_search_surname"
    JOB_TITLE_DATA = "employee_search_job_title"
    PROJECT_DATA = "employee_search_project"
    PATRONYMIC_DATA = "employee_search_patronymic"
    PERIOD_OF_TIME_DATA = "employee_search_period_of_time"


class EmployeeCardActionsButtons(Enum):
    EDIT_TEXT = "[📝] Редактировать"
    DELETE_TEXT = "[🗑️] Удалить"
    EDIT_DATA = "employee_card_update"
    DELETE_DATA = "employee_card_delete"


OPTIONAL_FIELD = "🚫 Не указывать"
DONT_UPDATE_FIELD = "🚫 Оставить текущее значение"
STOP_FILLING_FIELD = "🚫 Остановить заполнение"
