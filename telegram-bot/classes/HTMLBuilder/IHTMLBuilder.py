from abc import ABCMeta, abstractmethod


class IHTMLBuilder(metaclass=ABCMeta):
    """The builder design pattern interface"""

    @staticmethod
    @abstractmethod
    def build_id(id: str):
        """Method will build id of essence"""

    @staticmethod
    @abstractmethod
    def build_image(image_url: str):
        """Method will build image of essence"""

    @staticmethod
    @abstractmethod
    def build_datetime(unix_time: float):
        """Method will build datetime structure of essence"""

    @staticmethod
    @abstractmethod
    def get_result():
        """Returns the final structure essence"""
