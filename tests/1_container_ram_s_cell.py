# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-RAM
# 09 июл 2024

from G00_status_codes         import *
from G20_cactus_struct        import T20_StructCell
from G31_cactus_container_ram import C31_ContainerRAM

print("")
print("[== Тест Контейнера-RAM: S-Ячейка ==]")

container = C31_ContainerRAM()

cell = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="???", vlt=20)

result = container.ReadSCell(cell)
check  = result.code == CODES_COMPLETION.COMPLETED
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

result = container.WriteSCell(cell, flag_skip=False, flag_capture_delta=False)
check  = result.code == CODES_COMPLETION.COMPLETED
print("[+]" if check else "[ ]", "Запись без захвата изменений")

result = container.WriteSCell(cell, flag_skip=False, flag_capture_delta=False)
check  = result.code == CODES_COMPLETION.COMPLETED
print("[+]" if check else "[ ]", "Перезапись без захвата изменений")

result = container.WriteSCell(cell, flag_skip=True, flag_capture_delta=False)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_PROCESSING.SKIP in result.subcodes
print("[+]" if check else "[ ]", "Пропуск записи без захвата изменений")

result = container.DeleteSCell(cell, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print("[+]" if check else "[ ]", "Удаление c захватом изменений")

result = container.WriteSCell(cell, flag_skip=False, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print("[+]" if check else "[ ]", "Запись с захватом изменений")

cell = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="???", vlt=21)

result = container.WriteSCell(cell, flag_skip=False, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print("[+]" if check else "[ ]", "Перезапись c захватом изменений")

result = container.WriteSCell(cell, flag_skip=True, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_PROCESSING.SKIP in result.subcodes
check &= result.data is None
print("[+]" if check else "[ ]", "Пропуск записи с захватом изменений")

result = container.ReadSCell(cell)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print("[+]" if check else "[ ]", "Чтение")
