# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-RAM
# 16 июн 2024

from G00_status_codes         import *

from G20_cactus_struct        import T20_StructCell
from G31_cactus_container_ram import C31_ContainerRAM

print("")
print("[== Тест Контейнера-RAM: S-Ячейки ==]")

container = C31_ContainerRAM()

cells     = []

for index in range(10): cells.append(T20_StructCell("oci", "oid", f"pid_{index}", "cvl"))

result = container.ReadSCells(cells)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == 0
print(f"{'[+]' if check else '[ ]'} Чтение пакета S-Ячеек из пустого контейнера")

result = container.DeleteSCells(cells)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == 0
print(f"{'[+]' if check else '[ ]'} Удаление пакета S-Ячеек из пустого контейнера без захвата данных")

result = container.DeleteSCells(cells, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == 0
print(f"{'[+]' if check else '[ ]'} Удаление пакета S-Ячеек из пустого контейнера с захватом данных")

result = container.WriteSCells(cells)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == 0
print(f"{'[+]' if check else '[ ]'} Запись пакета S-Ячеек без захвата данных")

result = container.WriteSCells(cells, flag_skip=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == 0
print(f"{'[+]' if check else '[ ]'} Запись пакета S-Ячеек с пропуском без захвата данных")

result = container.WriteSCells(cells, flag_skip=True, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == 0
print(f"{'[+]' if check else '[ ]'} Запись пакета S-Ячеек с пропуском с захватом данных")

result = container.DeleteSCells(cells, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == len(cells)
print(f"{'[+]' if check else '[ ]'} Удаление пакета S-Ячеек с захватом данных")
