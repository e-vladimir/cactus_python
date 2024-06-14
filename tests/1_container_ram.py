# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-RAM

from G00_status_codes         import CODES_COMPLETION, CODES_PROCESSING

from G20_cactus_struct        import T20_StructCell
from G31_cactus_container_ram import C31_ContainerRAM

print("")
print("[== Тест Контейнера-RAM ==]")

container = C31_ContainerRAM()
result = len(container._s_cells) + len(container._d_cells)
check  = result == 0
print(f"{'[+]' if check else '[ ]'} Инициализация контейнера")

cell = T20_StructCell()
result = container.WriteSCell(cell, flag_capture_data=True)
check  = result.code != CODES_COMPLETION.COMPLETED
print(f"{'[+]' if check else '[ ]'} Отказ записи некорректной S-Ячейки")
check  = result.data.sid == cell.sid
print(f"{'[+]' if check else '[ ]'} Проверка захвата данных после отказа записи")

cell = T20_StructCell()
cell.oci = "1"
cell.oid = "2"
cell.pid = "3"
result = container.WriteSCell(cell, flag_capture_data=True)
check  = result.code == CODES_COMPLETION.COMPLETED
print(f"{'[+]' if check else '[ ]'} Запись корректной S-Ячейки")
check  = result.data.sid == cell.sid
print(f"{'[+]' if check else '[ ]'} Проверка захвата данных после записи")

cell.cvl = "100"
result = container.WriteSCell(cell, flag_mode_ignore=True, flag_capture_data=True)
check  = (result.code == CODES_COMPLETION.COMPLETED) and (CODES_PROCESSING.SKIP in result.subcodes)
print(f"{'[+]' if check else '[ ]'} Пропуск повторной записи S-Ячейки")
check  = result.data.cvl == ""
print(f"{'[+]' if check else '[ ]'} Проверка захвата данных после пропуска повторной записи")

result = container.WriteSCell(cell, flag_capture_data=True)
check  = (result.code == CODES_COMPLETION.COMPLETED)
print(f"{'[+]' if check else '[ ]'} Перезапись S-Ячейки")
check  = result.data.cvl == cell.cvl
print(f"{'[+]' if check else '[ ]'} Проверка захвата данных после перезаписи")

cell.cvl = "200"
cell.cut = 100
result = container.SyncSCell(cell, flag_capture_data=True)
check  = (result.code == CODES_COMPLETION.COMPLETED)
print(f"{'[+]' if check else '[ ]'} Синхронизация S-Ячейки с обновлением данных")
check  = result.data.cvl == "200"
print(f"{'[+]' if check else '[ ]'} Проверка захвата данных после синхронизации")

cell.cvl = "150"
cell.cut = 50
result = container.SyncSCell(cell, flag_capture_data=True)
check  = (result.code == CODES_COMPLETION.COMPLETED) and (CODES_PROCESSING.SKIP in result.subcodes)
print(f"{'[+]' if check else '[ ]'} Синхронизация S-Ячейки без обновления данных")
check  = result.data.cvl == "200"
print(f"{'[+]' if check else '[ ]'} Проверка захвата данных после синхронизации")

cell.cvl = ""
cell.cut = 0
result = container.ReadSCell(cell)
check  = (result.code == CODES_COMPLETION.COMPLETED) and (result.data.cvl == "200") and (result.data.cut == 100)
print(f"{'[+]' if check else '[ ]'} Чтение S-Ячейки")
