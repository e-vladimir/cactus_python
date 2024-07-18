# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-SQL.SQLite
# 12 июл 2024

import os
import time
from   copy import deepcopy

from G00_status_codes         import *

from G20_cactus_struct        import T20_StructCell

from G32_cactus_container_sql import C32_ContainerSQLite

print("")
print("[== Тест Контейнера-SQL.SQLite: Пакет S-Ячеек ==]")

try   : os.remove("./data.sqlite")
except: pass

container = C32_ContainerSQLite()
container.OptionsFilename("./data.sqlite")
container.Connect()

cell       = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="???", vlt=0)

time_0 = time.time()
result = container.RegisterClass(cell.idc)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "Регистрация класса")
if not check: print(f"                {result.code} {result.subcodes}\n")

cell        =  T20_StructCell(idc="idc")
cells       = [T20_StructCell(idc="idc", ido="ido", idp=f"idp_{index}", vlp=f"value_{index}", vlt=10) for index in range(10)]
cells_new   = [T20_StructCell(idc="idc", ido="ido", idp=f"idp_{index}", vlp=f"value_{index + 10}", vlt=20) for index in range(10)]
cells_old   = [T20_StructCell(idc="idc", ido="ido", idp=f"idp_{index}", vlp=f"value_{index + 10}", vlt=1) for index in range(10)]
cells_wrong = deepcopy(cells)
cells_wrong[4].ido = ""

time_0 = time.time()
result = container.ReadSCells(cell)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение пакета ячеек по маске из пустого контейнера")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.ReadSCells(cells)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение пакета ячеек по списку из пустого контейнера")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.ReadSCells(cells_wrong)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA       in result.subcodes
check &= CODES_DATA.ERROR_CHECK   in result.subcodes
check &= CODES_PROCESSING.PARTIAL in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение пакета ячеек по списку с некорректными параметрами из пустого контейнера")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.DeleteSCells(cell, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCells(cell)
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление пакета ячеек по маске из пустого контейнера (без захвата изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.DeleteSCells(cell, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление пакета ячеек по маске из пустого контейнера (с захватом изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.DeleteSCells(cells, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCells(cell)
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление пакета ячеек по списку из пустого контейнера (без захвата изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.DeleteSCells(cells_wrong, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.ERROR_CHECK in result.subcodes
check &= CODES_PROCESSING.PARTIAL in result.subcodes
result = container.ReadSCells(cell)
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление пакета ячеек по списку с некорректными параметрами из пустого контейнера (без захвата изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.DeleteSCells(cells, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление пакета ячеек по списку из пустого контейнера (с захватом изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.DeleteSCells(cells_wrong, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.ERROR_CHECK in result.subcodes
check &= CODES_PROCESSING.PARTIAL in result.subcodes
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление пакета ячеек по списку с некорректными параметрами из пустого контейнера (с захватом изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.WriteSCells(cells, False, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCells(cells)
check &= result.data == cells
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Запись пакета ячеек (без захвата изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.WriteSCells(cells_new, False, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCells(cell)
check &= result.data == cells_new
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Перезапись пакета ячеек (без захвата изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.WriteSCells(cells, True, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCells(cell)
check &= result.data == cells_new
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Пропуск перезаписи пакета ячеек (без захвата изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.WriteSCells(cells, False, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cells_new
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Перезапись пакета ячеек (с захватом изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.WriteSCells(cells_new, True, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Пропуск перезаписи пакета ячеек (с захватом изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.DeleteSCells(cell, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCells(cell)
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление пакета ячеек по маске (без захвата изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

container.WriteSCells(cells)

time_0 = time.time()
result = container.DeleteSCells(cell, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cells
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление пакета ячеек по маске (с захватом изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

container.WriteSCells(cells)

time_0 = time.time()
result = container.DeleteSCells(cells, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCells(cell)
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление пакета ячеек по списку (без захвата изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

container.WriteSCells(cells)

time_0 = time.time()
result = container.DeleteSCells(cells_wrong, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.ERROR_CHECK in result.subcodes
check &= CODES_PROCESSING.PARTIAL in result.subcodes
result = container.ReadSCells(cell)
check &= len(result.data) == 1
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление пакета ячеек по списку с некорректными параметрами (без захвата изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

container.WriteSCells(cells)

time_0 = time.time()
result = container.DeleteSCells(cells, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cells
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление пакета ячеек по списку (с захватом изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

container.WriteSCells(cells)

time_0 = time.time()
result = container.DeleteSCells(cells_wrong, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.ERROR_CHECK in result.subcodes
check &= CODES_PROCESSING.PARTIAL in result.subcodes
check &= len(result.data) == 9
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление пакета ячеек по списку с некорректными параметрами (с захватом изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

container.DeleteSCells(cell)

time_0 = time.time()
result = container.SyncSCells(cells, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCells(cell)
check &= result.data == cells
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Синхронизация пакета ячеек (без захвата изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.SyncSCells(cells, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCells(cell)
check &= result.data == cells
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Синхронизация пакета ячеек с пропуском (без захвата изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.SyncSCells(cells_new, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCells(cells)
check &= result.data == cells_new
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Синхронизация пакета ячеек с обновлением (без захвата изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

container.DeleteSCells(cell)

time_0 = time.time()
result = container.SyncSCells(cells, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cells
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Синхронизация пакета ячеек (с захватом изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.SyncSCells(cells, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Синхронизация пакета ячеек с пропуском (с захватом изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.SyncSCells(cells_new, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cells_new
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Синхронизация пакета ячеек с обновлением (с захватом изменений)")
if not check: print(f"                {result.code} {result.subcodes}\n")
