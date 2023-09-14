from .WorkerException import WorkerException


class NoSuchBucket(WorkerException):
    def __str__(self):
        return f"Couldn't find bucket"
