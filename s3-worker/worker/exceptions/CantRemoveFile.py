from .WorkerException import WorkerException


class CantRemoveFile(WorkerException):
    def __str__(self):
        return f"Couldn't remove file from bucket"
