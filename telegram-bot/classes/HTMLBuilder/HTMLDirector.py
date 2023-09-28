from .HTMLBuilder import HTMLBuilder


class HTMLDirector:
    """The Director, building a complex representation."""

    @staticmethod
    def construct():
        """Constructs and returns the final product"""
        return HTMLBuilder() \
            .build_id() \
            .build_part_b() \
            .build_part_c() \
            .get_result()
