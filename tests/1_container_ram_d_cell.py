# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-RAM
# 18 июн 2024

from G00_status_codes         import *

from G20_cactus_struct        import T20_StructCell
from G31_cactus_container_ram import C31_ContainerRAM

print("")
print("[== Тест Контейнера-RAM: D-Ячейка ==]")

container = C31_ContainerRAM()

cell      = T20_StructCell("oci", "oid", "pid", "cvl", 100)

result    = container.ReadDCell(cell)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (CODES_DATA.NO_DATA in result.subcodes)
check    &= (result.data        is None)
print(f"{'[+]' if check else '[ ]'} Чтение несуществующей D-Ячейки")

result    = container.WriteDCell(cell, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        == cell)
print(f"{'[+]' if check else '[ ]'} Запись D-Ячейки #100")

cell.cut = 101

result    = container.WriteDCell(cell, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        == cell)
print(f"{'[+]' if check else '[ ]'} Перезапись D-Ячейки #101")

container.Clear()

result    = container.DeleteDCell(cell, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        is None)
print(f"{'[+]' if check else '[ ]'} Удаление D-Ячейки из пустого контейнера")

result    = container.WriteDCell(cell, flag_capture_delta=True)
result    = container.DeleteDCell(cell, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        == cell)
print(f"{'[+]' if check else '[ ]'} Удаление D-Ячейки #101")
