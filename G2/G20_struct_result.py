# СТРУКТУРНЫЙ РЕЗУЛЬТАТ
# 08 июн 2024

from dataclasses      import (dataclass,
                              field)
from typing import Any

from G00_status_codes import CODES_COMPLETION, CODES


# ТИПЫ ДАННЫХ ОБЩЕГО НАЗНАЧЕНИЯ
@dataclass
class T20_StructResult:
	""" Результат-Код """
	code     : CODES_COMPLETION  = CODES_COMPLETION.COMPLETED
	subcodes : list[CODES] = field(default_factory=list)
	data     : Any | None        = None
