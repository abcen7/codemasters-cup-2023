from .WorkerException import WorkerException


class EnvironmentIncorrect(WorkerException):
    def __str__(self):
        return f"Environment is not defined or incorrect for S3 worker"
