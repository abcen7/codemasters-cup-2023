from .WorkerException import WorkerException


class UploadFileFailed(WorkerException):
    def __str__(self):
        return f"Couldn't upload file to bucket"
