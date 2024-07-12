# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-RAM
# 12 июл 2024

from G00_status_codes         import *
from G20_cactus_struct        import T20_StructCell
from G31_cactus_container_ram import C31_ContainerRAM

print("")
print("[== Тест Контейнера-RAM: D-Ячейка ==]")

container  = C31_ContainerRAM()

cell_wrong = T20_StructCell(idc="idc",            idp="idp", vlp="???", vlt=20)
cell       = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="???", vlt=20)

result = container.ReadDCell(cell_wrong)
check  = result.code == CODES_COMPLETION.INTERRUPTED
check &= CODES_DATA.ERROR_CHECK in result.subcodes
print("[+]" if check else "[ ]", "Чтение некорректной ячейки")

result = container.ReadDCell(cell)
check  = result.code == CODES_COMPLETION.INTERRUPTED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Чтение из пустого контейнера")

result = container.DeleteSCell(cell)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Удаление без захвата изменений")

result = container.DeleteSCell(cell, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Удаление с захватом изменений")

result = container.WriteDCell(cell)
result = container.ReadDCell(cell)
check  = result.code == CODES_COMPLETION.COMPLETED
print("[+]" if check else "[ ]", "Запись без захвата изменений")

result = container.DeleteDCell(cell, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print("[+]" if check else "[ ]", "Удаление c захватом изменений")

result = container.WriteDCell(cell, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print("[+]" if check else "[ ]", "Запись с захватом изменений")

result = container.WriteDCell(cell, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_PROCESSING.SKIP in result.subcodes
print("[+]" if check else "[ ]", "Пропуск при перезаписи")

result = container.ReadDCell(cell)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print("[+]" if check else "[ ]", "Чтение")
