# ТЕСТИРОВАНИЕ ПРОИЗВОДЕЛЬНОСТИ КАКТУС-21
# 24 окт 2024

import os
import time

import pytest

from G00_status_codes         import *

from G20_cactus_struct        import T20_StructCell

from G32_cactus_container_sql import C32_ContainerSQLite

print("")
print("[== Тест Контейнера-SQL.SQLite: Производительность Кактус 21 ==]")

try   : os.remove("./data.sqlite")
except: pass

container = C32_ContainerSQLite()
container.OptionsFilename("./data")
container.Connect()

cell       = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="???", vlt=0)

time_0 = time.time()
result = container.RegisterClass(cell.idc)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
print(f"{(time_1 - time_0):0.3f} сек   Подготовка контейнера")
if not check: print(f"                  {result.code} {result.subcodes}\n")

size   = 100

cell   =  T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="val", vlt=0)
cells  = [T20_StructCell(idc="idc", ido="ido", idp=f"idp_{index}", vlp="val", vlt=0) for index in range(size)]

def s_cells_rewrite():
    time_0 = time.time()
    for index in range(size): container.WriteSCell(cell, False, False)
    time_1 = time.time()
    time_delta = time_1 - time_0
    print(f"{time_delta/size:0.3f} сек   Перезапись 1 S-Ячейки")

@pytest.mark.perfomance
def test_cells_rewrite(benchmark):
    benchmark(s_cells_rewrite)


def s_cells_write():
    time_0 = time.time()
    for cell in cells: container.WriteSCell(cell, False, False)
    time_1 = time.time()
    time_delta = time_1 - time_0
    print(f"{time_delta/size:0.3f} сек   Запись 1 S-Ячейки")

@pytest.mark.perfomance
def test_s_cells_write(benchmark):
    benchmark(s_cells_write)


def s_cells_delete():
    time_0 = time.time()
    for cell in cells: container.DeleteSCell(cell, False)
    time_1 = time.time()
    time_delta = time_1 - time_0
    print(f"{time_delta/size:0.3f} сек   Удаление 1 S-Ячейки")

@pytest.mark.perfomance
def test_s_cells_delete(benchmark):
    benchmark(s_cells_delete)

def s_pkg_write():
    time_0 = time.time()
    container.WriteSCells(cells, False, False)
    time_1 = time.time()
    time_delta = time_1 - time_0
    print(f"{time_delta:0.3f} сек   Запись пакета S-Ячеек ({size})")

@pytest.mark.perfomance
def test_s_pkg_write(benchmark):
    benchmark(s_pkg_write)