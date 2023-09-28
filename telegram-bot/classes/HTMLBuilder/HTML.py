class HTML:
    """The Product"""
    NEW_LINE = "\n"

    def __init__(
            self,
            id: str,
    ):
        self.id

    def __str__(self):
        return self.NEW_LINE.join(self.parts)

