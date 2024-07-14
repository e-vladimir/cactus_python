# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-RAM
# 14 июл 2024

from G00_status_codes         import *
from G20_cactus_struct        import T20_StructCell
from G21_cactus_struct        import T21_VltRange

from G31_cactus_container_ram import C31_ContainerRAM

print("")
print("[== Тест Контейнера-RAM: Пакет D-Ячеек ==]")

cell_range =  T21_VltRange(idc="idc", ido="ido", idp="idp")
cells      = [T20_StructCell(idc="idc", ido="ido", idp="idp", vlp=f"value_{index}", vlt=index) for index in range(1, 11)]

container  = C31_ContainerRAM()

result = container.ReadDCells(cell_range)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Чтение пакета ячеек из пустого контейнера")

for cell in cells: container.WriteDCell(cell)

result = container.ReadDCells(cell_range)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == len(cells)
print("[+]" if check else "[ ]", "Чтение пакета ячеек")

result = container.DeleteDCells(cell_range, False)
check  = result.code == CODES_COMPLETION.COMPLETED
result = container.ReadDCells(cell_range)
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Удаление пакета ячеек без захвата изменений")

for cell in cells: container.WriteDCell(cell)

result = container.DeleteDCells(cell_range, True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == len(cells)
print("[+]" if check else "[ ]", "Удаление пакета ячеек с захватом изменений")
