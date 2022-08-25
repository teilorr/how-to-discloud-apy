from __future__ import annotations
from typing import (
    Optional, 
    Any
)

import re

class DotEnv:
    _path_env_file = ".env"

    def __init__(self, /, *, env_file: Optional[str]=".env") -> None:
        self._path_env_file = env_file

    @classmethod
    def with_custom_file(cls, new_file: str) -> DotEnv:
        return cls(env_file=new_file)

    @classmethod
    def get(cls, var_name: str) -> Any:
        find_numbers_regex = r"^-?\d+(\d+)$"

        with open(cls._path_env_file, "r", encoding="UTF-8") as f:
            for line in f:
                line: str = line.replace("\n", "").strip()
                
                if not line or line.startswith("#"):
                    continue

                key, value = line.split("=", maxsplit=1)

                if key.strip() == var_name.strip():
                    if re.match(find_numbers_regex, value) is not None:
                        value = int(value)
                    return value
