# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-RAM
# 08 июл 2024

from G00_status_codes         import *

from G20_cactus_struct        import T20_StructCell
from G21_cactus_struct import T21_VltRange
from G31_cactus_container_ram import C31_ContainerRAM

print("")
print("[== Тест Контейнера-RAM: D-Ячейки ==]")

container = C31_ContainerRAM()

cells     = list(T20_StructCell("idc", "ido", f"idp", "vlp", index) for index in range(10))
vlt_range = T21_VltRange("idc", "ido", f"idp", "vlp")

result    = container.ReadDCells(vlt_range)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 0)
print(f"{'[+]' if check else '[ ]'} Чтение пакета D-Ячеек из пустого контейнера")

for cell in cells: container.WriteDCell(cell)

result    = container.ReadDCells(vlt_range)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 10)
print(f"{'[+]' if check else '[ ]'} Чтение пакета D-Ячеек")

result    = container.ReadDVlts(T21_VltRange("idc", "ido", "idp"))
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 10)
print(f"{'[+]' if check else '[ ]'} Чтение списка VLT D-Ячеек через IDC.IDO.IDP")

result    = container.ReadDVlts(T21_VltRange("idc", "ido", "idp", vlt_l=4, vlt_r=8))
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 3)
print(f"{'[+]' if check else '[ ]'} Чтение списка VLT D-Ячеек через IDC.IDO.IDP [VLT_L - VLT_R]")

result    = container.ReadDVltRange(T21_VltRange("idc", "ido", "idp"))
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (result.data is not None)
check    &= (result.data.vlt_l == 0)
check    &= (result.data.vlt_r == 9)
print(f"{'[+]' if check else '[ ]'} Чтение границ VLT D-Ячеек через IDC.IDO.IDP")

result    = container.ReadDVltRange(T21_VltRange("idc", "ido", "idp", vlt_l=4, vlt_r=8))
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (result.data is not None)
check    &= (result.data.vlt_l == 5)
check    &= (result.data.vlt_r == 7)
print(f"{'[+]' if check else '[ ]'} Чтение границ VLT D-Ячеек через IDC.IDO.IDP [VLT_L - VLT_R]")

result    = container.DeleteDCells(vlt_range, flag_capture_delta=True)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 10)
print(f"{'[+]' if check else '[ ]'} Удаление пакета D-Ячеек")
