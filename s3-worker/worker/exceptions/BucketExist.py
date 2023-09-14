from .WorkerException import WorkerException


class BucketExist(WorkerException):
    def __str__(self):
        return f"Bucket already exist"
