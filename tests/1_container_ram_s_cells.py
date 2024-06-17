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
print(f"{'[+]' if check else '[ ]'} Чтение S-Ячеек из пустого контейнера")

result = container.WriteSCells(cells, flag_capture_delta=True)
print(result)
