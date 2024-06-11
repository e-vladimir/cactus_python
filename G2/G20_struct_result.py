# СТРУКТУРНЫЙ РЕЗУЛЬТАТ
# 11 июн 2024

from dataclasses      import (dataclass,
                              field)
from typing           import Any

from G00_status_codes import CODES_COMPLETION, CODES


@dataclass
class T20_StructResult:
	""" Структурный результат """
	code     : CODES_COMPLETION = CODES_COMPLETION.COMPLETED
	subcodes : set[CODES]       = field(default_factory=set)
	data     : Any | None       = None
