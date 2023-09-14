from .WorkerException import WorkerException


class CantRemoveBucket(WorkerException):
    def __str__(self):
        return f"Couldn't remove bucket"
