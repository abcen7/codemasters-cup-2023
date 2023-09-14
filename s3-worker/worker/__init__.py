import mimetypes
from typing import NoReturn, BinaryIO
from os import path

import boto3
from botocore.exceptions import ClientError

from .Singleton import Singleton
from .exceptions import \
    EnvironmentIncorrect, \
    WorkerDoesNotStarted, \
    UploadFileFailed, \
    CantGetFile, \
    CantRemoveFile, \
    CantRemoveBucket, \
    NoSuchBucket, \
    BucketExist

from .config import \
    MINIO_ACCESS_KEY, \
    MINIO_SECRET_KEY, \
    MINIO_ENDPOINT_URL, \
    MINIO_EXPIRES_FILE_LINK_IN_SECONDS


class File:
    filename: str
    mimetype: str
    data: BinaryIO

    def __init__(self,
                 filename: str = None,
                 mimetype: str = None,
                 data: BinaryIO = None,
                 filepath: str = None):

        if filepath:
            mimetype = mimetype or mimetypes.guess_type(filepath)[0]
            filename = filename or path.basename(filepath)
            data = data or open(filepath, "rb")

        self.mimetype = mimetype
        self.filename = filename
        self.data = data


class S3Worker(Singleton):
    S3 = "s3"

    ENVIRONMENT_LIST = [
        MINIO_SECRET_KEY,
        MINIO_ACCESS_KEY,
        MINIO_ENDPOINT_URL
    ]

    def __init__(self):
        """
        Initializing the s3 client
        """
        for item in self.ENVIRONMENT_LIST:
            if not item:
                raise EnvironmentIncorrect
        self.s3 = boto3.client(
            self.S3,
            endpoint_url=MINIO_ENDPOINT_URL,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY
        )
        if not self.s3:
            raise WorkerDoesNotStarted

    def new_bucket(self, bucket_name: str) -> NoReturn:
        """
        Creating the bucket
        :param bucket_name: name of the bucket
        """
        try:
            self.s3.create_bucket(Bucket=bucket_name)
        except ClientError:
            raise BucketExist

    def upload_file(self, bucket_name: str, file: File) -> str:
        """
        Uploading a file to bucket
        :param bucket_name: name of the bucket, where the file will be uploaded
        :param file: file, which would be uploaded
        """
        try:
            self.s3.upload_fileobj(
                file.data,
                bucket_name,
                file.filename,
                ExtraArgs={"ContentType": file.mimetype}
            )
            #import time
            #time.sleep(1)
            return self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": file.filename},
                ExpiresIn=MINIO_EXPIRES_FILE_LINK_IN_SECONDS
            )
        except ClientError:
            raise UploadFileFailed

    def get_file_url(self, bucket_name: str, file_name: str):
        """
        :param bucket_name: name of the bucket, where the file will be uploaded
        :param file_name: name of the file
        """
        try:
            url = self.s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": bucket_name, "Key": file_name},
                ExpiresIn=MINIO_EXPIRES_FILE_LINK_IN_SECONDS
            )
            return url
        except ClientError:
            raise CantGetFile

    def remove_file(self, bucket_name: str, file_name: str) -> NoReturn:
        """
        :param bucket_name: name of the bucket, where the file will be deleted
        :param file_name: name of the file
        """
        try:
            self.s3.delete_object(Bucket=bucket_name, Key=file_name)
        except ClientError:
            raise CantRemoveFile

    def remove_bucket(self, bucket_name: str) -> NoReturn:
        """
        :param bucket_name: name of the bucket to delete
        """
        try:
            for file_name in self.list_files(bucket_name):
                self.remove_file(bucket_name, file_name)

            self.s3.delete_bucket(Bucket=bucket_name)
        except ClientError:
            raise CantRemoveBucket

    def list_files(self, bucket_name: str) -> list[str]:
        """
        Return all objects of the bucket
        :param bucket_name: name of the bucket, where the file will be uploaded
        """
        try:
            objects = self.s3.list_objects(Bucket=bucket_name)

            if "Contents" in objects:
                return list(map(lambda x: x["Key"], objects["Contents"]))
            return []
        except ClientError:
            raise NoSuchBucket
