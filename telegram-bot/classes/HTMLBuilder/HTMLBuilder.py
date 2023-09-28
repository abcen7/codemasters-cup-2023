import datetime

from .IHTMLBuilder import IHTMLBuilder
from .HTML import HTML


class HTMLBuilder(IHTMLBuilder):
    """HTMLBuilder - building the html from Rest - API essence"""

    def __init__(self):
        self.product = HTML()

    def build_id(self, id: str):
        self.product.parts.append(
            f'<b>ID: </b><pre>{id}</pre>'
        )
        return self

    def build_image(self, image_url: str):
        self.product.parts.append(
            f'<a href="{image_url}">&#8205;</a>'
        )
        return self

    def build_datetime(self, unix_time: float):
        self.product.parts.append(
            f'<b>Дата прихода</b>: {datetime.datetime.fromtimestamp(unix_time)}'
        )
        return self

    def get_result(self):
        return str(self.product)
