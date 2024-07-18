# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-RAM
# 16 июл 2024

import time

from G00_status_codes         import *
from G20_cactus_struct        import T20_StructCell
from G21_cactus_struct        import T21_VltRange

from G31_cactus_container_ram import C31_ContainerRAM

print("")
print("[== Тест Контейнера-RAM: Пакет D-Ячеек ==]")

container  = C31_ContainerRAM()

cell_range =  T21_VltRange(idc="idc", ido="ido", idp="idp")
cells      = [T20_StructCell(idc="idc", ido="ido", idp="idp", vlp=f"value_{index}", vlt=index) for index in range(1, 11)]

time_0 = time.time()
result = container.ReadDCells(cell_range)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение пакета ячеек из пустого контейнера")
if not check: print(f"                {result.code} {result.subcodes}\n")

for cell in cells: container.WriteDCell(cell)

time_0 = time.time()
result = container.ReadDCells(cell_range)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == len(cells)
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение пакета ячеек")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.ReadVltRange(T21_VltRange(idc="idc", ido="ido", idp="idp"))
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data.vlt_l ==  1
check &= result.data.vlt_r == 10
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение границ VLT")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.ReadVlts(T21_VltRange(idc="idc", ido="ido", idp="idp"))
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == 10
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение списка VLT")
if not check: print(f"                {result.code} {result.subcodes}\n")

time_0 = time.time()
result = container.DeleteDCells(cell_range, False)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadDCells(cell_range)
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление пакета ячеек без захвата изменений")
if not check: print(f"                {result.code} {result.subcodes}\n")

for cell in cells: container.WriteDCell(cell)

time_0 = time.time()
result = container.DeleteDCells(cell_range, True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == len(cells)
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление пакета ячеек с захватом изменений")
if not check: print(f"                {result.code} {result.subcodes}\n")
