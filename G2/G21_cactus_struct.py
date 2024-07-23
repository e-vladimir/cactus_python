# КАКТУС: СТРУКТУРЫ ДАННЫХ
# 23 июл 2024

import s3m

from   dataclasses       import (dataclass,
                                 field)

from   psycopg2          import extensions

from   G20_cactus_struct import T20_StructCell
from   G20_struct_result import T20_StructResult


# ТИПЫ ДАННЫХ СТРУКТУРНОЙ ЯЧЕЙКИ
@dataclass
class T21_VltRange(T20_StructCell):
	""" Диапазон VLT """
	vlt_l: int = 0  # Левая граница диапазона (меньшее)
	vlt_r: int = 0  # Правая граница диапазона (большее)


@dataclass
class T21_StructResult_StructCell(T20_StructResult):
	""" Результат - Структурная ячейка """
	data: T20_StructCell | None = None


@dataclass
class T21_StructResult_StructCells(T20_StructResult):
	""" Результат - Список структурных ячеек """
	data: list[T20_StructCell] = field(default_factory=list)


@dataclass
class T21_StructResult_VltRange(T20_StructResult):
	""" Результат - Диапазон VLT """
	data: T21_VltRange | None = None


# ТИПЫ ДАННЫХ SQL КОНТЕЙНЕРА
@dataclass
class T21_StructResult_CursorS3m(T20_StructResult):
	""" Результат-Курсор """
	cursor : s3m.Cursor | None = None


@dataclass
class T21_StructResult_CursorPostgresql(T20_StructResult):
	""" Результат-Курсор """
	cursor : extensions.cursor | None = None
