# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-SQL.SQLite
# 18 июл 2024

import os
import time

from G30_cactus_struct import T30_StructCell
from G32_cactus_container_sql import C32_ContainerSQLite

print("")
print("[== Тест Контейнера-SQL.SQLite: Производительность Кактус 20 ==]")

try   : os.remove("./data.sqlite")
except: pass

container = C32_ContainerSQLite()
container.OptionsFilename("./data.sqlite")
container.Connect()

cell       = T30_StructCell("idc", "ido", "idp", "???", 0)

time_0 = time.time()
container.RegisterClass(cell.oci)
time_1 = time.time()
print(f"{(time_1 - time_0):0.3f} сек   Подготовка контейнера")

size   = 100

cell   =  T30_StructCell("idc", "ido",  "idp",         "val", 0)
cells  = [T30_StructCell("idc", "ido", f"idp_{index}", "val", 0) for index in range(size)]

time_0 = time.time()
for index in range(size): container.WriteSCell(cell, False)
time_1 = time.time()
time_delta = time_1 - time_0
print(f"{time_delta/size:0.3f} сек   Перезапись 1 S-Ячейки")

time_0 = time.time()
for cell in cells: container.WriteSCell(cell, False)
time_1 = time.time()
time_delta = time_1 - time_0
print(f"{time_delta/size:0.3f} сек   Запись 1 S-Ячейки")

time_0 = time.time()
for cell in cells: container.DeleteSCell(cell)
time_1 = time.time()
time_delta = time_1 - time_0
print(f"{time_delta/size:0.3f} сек   Удаление 1 S-Ячейки")

time_0 = time.time()
container.WriteSCells(cells)
time_1 = time.time()
time_delta = time_1 - time_0
print(f"{time_delta:0.3f} сек   Запись пакета S-Ячеек ({size})")
