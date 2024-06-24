# КАКТУС: СТРУКТУРЫ ДАННЫХ
# 15 июн 2024

import s3m

from   dataclasses       import (dataclass,
                                 field)

from   G20_cactus_struct import T20_StructCell
from   G20_struct_result import T20_StructResult


# ТИПЫ ДАННЫХ СТРУКТУРНОЙ ЯЧЕЙКИ
@dataclass
class T21_CutRange(T20_StructCell):
	""" Диапазон CUT """
	cut_l: int = 0  # Левая граница диапазона (меньшее)
	cut_r: int = 0  # Правая граница диапазона (большее)


@dataclass
class T21_StructResult_StructCell(T20_StructResult):
	""" Результат - Структурная ячейка """
	data: T20_StructCell | None = None


@dataclass
class T21_StructResult_StructCells(T20_StructResult):
	""" Результат - Список структурных ячеек """
	data: list[T20_StructCell] = field(default_factory=list)


@dataclass
class T21_StructResult_CutRange(T20_StructResult):
	""" Результат - Диапазон CUT """
	data: T21_CutRange | None = None


# ТИПЫ ДАННЫХ SQL КОНТЕЙНЕРА
@dataclass
class T31_StructResult_CursorS3m(T20_StructResult):
	""" Результат-Курсор """
	cursor : s3m.Cursor | None = None
