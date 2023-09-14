from .WorkerException import WorkerException


class WorkerDoesNotStarted(WorkerException):
    def __str__(self):
        return f"S3 worker was not started"
