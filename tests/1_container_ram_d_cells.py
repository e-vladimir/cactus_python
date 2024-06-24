# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-RAM
# 19 июн 2024

from G00_status_codes         import *

from G20_cactus_struct        import T20_StructCell
from G21_cactus_struct import T21_CutRange
from G31_cactus_container_ram import C31_ContainerRAM

print("")
print("[== Тест Контейнера-RAM: D-Ячейки ==]")

container = C31_ContainerRAM()

cells     = list(T20_StructCell("oci", "oid", f"pid", "cvl", index) for index in range(10))
cut_range = T21_CutRange("oci", "oid", f"pid", "cvl")

result    = container.ReadDCells(cut_range)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 0)
print(f"{'[+]' if check else '[ ]'} Чтение пакета D-Ячеек из пустого контейнера")

for cell in cells: container.WriteDCell(cell)

result    = container.ReadDCells(cut_range)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 10)
print(f"{'[+]' if check else '[ ]'} Чтение пакета D-Ячеек")

result    = container.ReadDCuts(T21_CutRange("oci", "oid", "pid"))
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 10)
print(f"{'[+]' if check else '[ ]'} Чтение списка CUT D-Ячеек через OCI.OID.PID")

result    = container.ReadDCuts(T21_CutRange("oci", "oid", "pid", cut_l=4, cut_r=8))
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 3)
print(f"{'[+]' if check else '[ ]'} Чтение списка CUT D-Ячеек через OCI.OID.PID [CUT_L - CUT_R]")

result    = container.ReadDCutRange(T21_CutRange("oci", "oid", "pid"))
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (result.data is not None)
check    &= (result.data.cut_l == 0)
check    &= (result.data.cut_r == 9)
print(f"{'[+]' if check else '[ ]'} Чтение границ CUT D-Ячеек через OCI.OID.PID")

result    = container.ReadDCutRange(T21_CutRange("oci", "oid", "pid", cut_l=4, cut_r=8))
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (result.data is not None)
check    &= (result.data.cut_l == 5)
check    &= (result.data.cut_r == 7)
print(f"{'[+]' if check else '[ ]'} Чтение границ CUT D-Ячеек через OCI.OID.PID [CUT_L - CUT_R]")

result    = container.DeleteDCells(cut_range, flag_capture_delta=True)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 10)
print(f"{'[+]' if check else '[ ]'} Удаление пакета D-Ячеек")
