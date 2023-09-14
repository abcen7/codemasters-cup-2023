from .WorkerException import WorkerException


class CantGetFile(WorkerException):
    def __str__(self):
        return f"Couldn't generate file url"
