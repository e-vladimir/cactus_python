# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-RAM
# 01 ноя 2024

import time

from G00_status_codes         import *

from G20_cactus_struct        import T20_StructCell

from G31_cactus_container_ram import C31_ContainerRAM

print("")
print("[== Тест Контейнера-RAM: S-Ячейка ==]")

container = C31_ContainerRAM()

cell       = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="???", vlt=0)
cell_wrong = T20_StructCell(idc="idc",            idp="idp", vlp="???", vlt=0)

time_0 = time.time()
result = container.ReadSCell(cell_wrong)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.INTERRUPTED
check &= CODES_DATA.ERROR_CHECK in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Попытка чтения ячейки с некорректными данными")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.ReadSCell(cell)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение несуществующей ячейки")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.DeleteSCell(cell_wrong, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.INTERRUPTED
check &= CODES_DATA.ERROR_CHECK in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Попытка удаления ячейки с некорректными данными (без захвата изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.DeleteSCell(cell, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление несуществующей ячейки (без захвата изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.DeleteSCell(cell, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление несуществующей ячейки (с захватом изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.WriteSCell(cell_wrong, False, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.INTERRUPTED
check &= CODES_DATA.ERROR_CHECK in result.subcodes
result = container.ReadSCell(cell)
check &= result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Попытка записи ячейки с некорректными данными (без пропуска, без захвата изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.WriteSCell(cell, False, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCell(cell)
check &= result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Запись ячейки (без пропуска, без захвата изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

cell.vlp = "123"

time_0 = time.time()
result = container.WriteSCell(cell, False, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCell(cell)
check &= result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Перезапись ячейки (без пропуска, без захвата изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

cell.vlp = "321"

time_0 = time.time()
result = container.WriteSCell(cell, False, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Перезапись ячейки (без пропуска, c захватом изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

cell.vlp = "111"

time_0 = time.time()
result = container.WriteSCell(cell, True, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_PROCESSING.SKIP in result.subcodes
result = container.ReadSCell(cell)
check &= result.data.vlp == "321"
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Пропуск перезаписи ячейки (без захвата изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.WriteSCell(cell, True, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_PROCESSING.SKIP in result.subcodes
result = container.ReadSCell(cell)
check &= result.data.vlp == "321"
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Пропуск перезаписи ячейки (с захватом изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.DeleteSCell(cell, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCell(cell)
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление ячейки (без захвата изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.WriteSCell(cell, False, False)
result = container.DeleteSCell(cell, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление ячейки (с захватом изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.SyncSCell(cell_wrong, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.INTERRUPTED
check &= CODES_DATA.ERROR_CHECK in result.subcodes
result = container.ReadSCell(cell)
check &= result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Попытка синхронизации ячейки с некорректными данными (без захвата изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.SyncSCell(cell, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCell(cell)
check &= result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Синхронизация ячейки (запись) (без захвата изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

cell.vlt = 1

time_0 = time.time()
result = container.SyncSCell(cell, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCell(cell)
check &= result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Синхронизация ячейки (обновление) (без захвата изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

cell.vlt = 0

time_0 = time.time()
result = container.SyncSCell(cell, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadSCell(cell)
check &= result.code == CODES_COMPLETION.COMPLETED
check &= result.data.vlt == 1
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Синхронизация ячейки (пропуск) (без захвата изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

cell.vlt = 2

time_0 = time.time()
result = container.SyncSCell(cell, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Синхронизация ячейки (обновление) (с захватом изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")

cell.vlt = 0

time_0 = time.time()
result = container.SyncSCell(cell, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_PROCESSING.SKIP in result.subcodes
check &= result.data.vlt == 2
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Синхронизация ячейки (пропуск) (с захватом изменений)")
if not check: print(f"                  {result.code} {result.subcodes}\n")
