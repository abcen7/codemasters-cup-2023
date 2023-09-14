from datetime import datetime

import time


def get_current_time_in_unix_format() -> float:
    """
    Get time in Unix
    """
    return time.mktime(datetime.now().timetuple())
