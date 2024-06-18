# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-RAM
# 16 июн 2024

from G00_status_codes         import *

from G20_cactus_struct        import T20_StructCell
from G31_cactus_container_ram import C31_ContainerRAM

print("")
print("[== Тест Контейнера-RAM: S-Ячейки ==]")

container = C31_ContainerRAM()

cells     = list(T20_StructCell("oci", "oid", f"pid_{index}", "cvl") for index in range(10))

result    = container.ReadSCells(cells)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 0)
print(f"{'[+]' if check else '[ ]'} Чтение пакета S-Ячеек из пустого контейнера")

result    = container.DeleteSCells(cells, flag_capture_delta=False)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 0)
print(f"{'[+]' if check else '[ ]'} Удаление пакета S-Ячеек из пустого контейнера без захвата изменений")

result    = container.DeleteSCells(cells, flag_capture_delta=True)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 0)
print(f"{'[+]' if check else '[ ]'} Удаление пакета S-Ячеек из пустого контейнера c захватом изменений")

result    = container.WriteSCells(cells, flag_skip=False, flag_capture_delta=False)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 0)
print(f"{'[+]' if check else '[ ]'} Запись пакета S-Ячеек без пропуска и без захвата изменений")

result    = container.WriteSCells(cells, flag_skip=False, flag_capture_delta=False)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 0)
print(f"{'[+]' if check else '[ ]'} Перезапись пакета S-Ячеек без пропуска и без захвата изменений")

result    = container.WriteSCells(cells, flag_skip=True, flag_capture_delta=False)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (CODES_PROCESSING.PARTIAL in result.subcodes)
check    &= (len(result.data) == 0)
print(f"{'[+]' if check else '[ ]'} Перезапись пакета S-Ячеек c пропуском и без захвата изменений")

result    = container.ReadSCells(T20_StructCell("oci", "oid"))
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == len(cells))
print(f"{'[+]' if check else '[ ]'} Чтение пакета ячеек по OCI.OID")

result    = container.ReadSCells(cells)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == len(cells))
print(f"{'[+]' if check else '[ ]'} Чтение пакета ячеек по OCI.OID.PID")

result    = container.DeleteSCells(T20_StructCell("oci", "oid"), flag_capture_delta=True)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == len(cells))
print(f"{'[+]' if check else '[ ]'} Удаление пакета S-Ячеек по OCI.OID c захватом изменений")

result    = container.WriteSCells(cells, flag_skip=False, flag_capture_delta=False)
result    = container.DeleteSCells(cells, flag_capture_delta=True)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == len(cells))
print(f"{'[+]' if check else '[ ]'} Удаление пакета S-Ячеек по OCI.OID.PID c захватом изменений")

container.Clear()

result    = container.SyncSCells(cells, flag_capture_delta=False)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == 0)
print(f"{'[+]' if check else '[ ]'} Синхронизация пакета S-Ячеек без захвата изменений")

container.Clear()

cells     = list(T20_StructCell("oci", "oid", f"pid_{index}", "cvl", 0) for index in range(10))
result    = container.SyncSCells(cells, flag_capture_delta=True)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == len(cells))
print(f"{'[+]' if check else '[ ]'} Синхронизация пакета S-Ячеек с захватом изменений")

cells     = list(T20_StructCell("oci", "oid", f"pid_{index}", "cvl", index) for index in range(10))
result    = container.SyncSCells(cells, flag_capture_delta=True)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (len(result.data) == (len(cells) - 1))
print(f"{'[+]' if check else '[ ]'} Синхронизация пакета S-Ячеек на новые с захватом изменений")
