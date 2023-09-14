from datetime import datetime

import time
from typing import List, Dict


def get_current_time_in_unix_format() -> float:
    """
    Get time in Unix
    """
    return time.mktime(datetime.now().timetuple())


def prepare_model_for_search_query(model: Dict[str, str]) -> List[Dict[str, Dict[str, str]]]:
    return [{key: {"$regex": f"{model[key]}", "$options": "i"}} for key in model]
