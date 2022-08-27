from utils.dotenv import DotEnv
from utils.route import Route

import re

def is_number(obj) -> bool:
    return bool(re.match(r"^-?\d+(\d+)$", obj))