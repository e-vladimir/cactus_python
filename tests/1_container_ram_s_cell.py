# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-RAM
# 16 июн 2024

from G00_status_codes         import *

from G20_cactus_struct        import T20_StructCell
from G31_cactus_container_ram import C31_ContainerRAM

print("")
print("[== Тест Контейнера-RAM: S-Ячейка ==]")

container = C31_ContainerRAM()

cell      = T20_StructCell("oci", "oid", "pid", "cvl", 0)

result    = container.DeleteSCell(cell)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (CODES_DATA.NO_DATA in result.subcodes)
check    &= (result.data        is None)
print(f"{'[+]' if check else '[ ]'} Удаление S-Ячейки из пустого контейнера без захвата изменений")

result    = container.DeleteSCell(cell, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (CODES_DATA.NO_DATA in result.subcodes)
check    &= (result.data        is None)
print(f"{'[+]' if check else '[ ]'} Удаление S-Ячейки из пустого контейнера с захватом изменений")

result    = container.WriteSCell(cell, flag_skip=False, flag_capture_delta=False)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        is None)
print(f"{'[+]' if check else '[ ]'} Запись S-Ячейки без захвата изменений")

result    = container.DeleteSCell(cell, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        is not None)
print(f"{'[+]' if check else '[ ]'} Удаление S-Ячейки с захватом изменений")

result    = container.WriteSCell(cell, flag_skip=False, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        is not None)
print(f"{'[+]' if check else '[ ]'} Запись S-Ячейки с захватом изменений")

result    = container.WriteSCell(cell, flag_skip=False, flag_capture_delta=True)
check     = (result.code           == CODES_COMPLETION.COMPLETED)
check    &= (result.data           is None)
print(f"{'[+]' if check else '[ ]'} Перезапись S-Ячейки с захватом изменений")

cell.cut  = 10

result    = container.WriteSCell(cell, flag_skip=False, flag_capture_delta=True)
check     = (result.code           == CODES_COMPLETION.COMPLETED)
check    &= (result.data           is not None)
print(f"{'[+]' if check else '[ ]'} Перезапись S-Ячейки с новыми данными с захватом изменений")

result    = container.WriteSCell(cell, flag_skip=True, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        is None)
print(f"{'[+]' if check else '[ ]'} Перезапись S-Ячейки с пропуском и захватом изменений")

cell      = T20_StructCell()

result    = container.ReadSCell(cell)
check     = (result.code            == CODES_COMPLETION.INTERRUPTED)
check    &= (CODES_DATA.ERROR_CHECK in result.subcodes)
check    &= (result.data            is None)
print(f"{'[+]' if check else '[ ]'} Отказ чтения S-Ячейки с некорректными параметрами (OCI, OID, PID)")

cell      = T20_StructCell(oci="oci")

result    = container.ReadSCell(cell)
check     = (result.code            == CODES_COMPLETION.INTERRUPTED)
check    &= (CODES_DATA.ERROR_CHECK in result.subcodes)
check    &= (result.data            is None)
print(f"{'[+]' if check else '[ ]'} Отказ чтения S-Ячейки с некорректными параметрами (OID, PID)")

cell      = T20_StructCell(oci="oci", oid="oid")

result    = container.ReadSCell(cell)
check     = (result.code            == CODES_COMPLETION.INTERRUPTED)
check    &= (CODES_DATA.ERROR_CHECK in result.subcodes)
check    &= (result.data            is None)
print(f"{'[+]' if check else '[ ]'} Отказ чтения S-Ячейки с некорректными параметрами (PID)")

cell      = T20_StructCell(oci="oci", oid="oid", pid="pid")

result    = container.ReadSCell(cell)
check     = (result.code            == CODES_COMPLETION.COMPLETED)
check    &= (result.data            is not None)
check    &= (result.data.cut        == 10)
print(f"{'[+]' if check else '[ ]'} Чтение S-Ячейки")

cell      = T20_StructCell("oci", "", "pid", "cvl", cut=11)

result    = container.SyncSCell(cell, flag_capture_delta=True)
check     = (result.code            == CODES_COMPLETION.INTERRUPTED)
check    &= (CODES_DATA.ERROR_CHECK in result.subcodes)
check    &= (result.data            is None)
print(f"{'[+]' if check else '[ ]'} Отказ синхронизации некорректной S-Ячейки")

cell      = T20_StructCell("oci", "oid", "pid", "cvl", cut=9)

result    = container.SyncSCell(cell, flag_capture_delta=True)
check     = (result.code           == CODES_COMPLETION.COMPLETED)
check    &= (CODES_PROCESSING.SKIP in result.subcodes)
check    &= (result.data.cut       == 10)
print(f"{'[+]' if check else '[ ]'} Синхронизация устаревшей S-Ячейки")

cell      = T20_StructCell("oci", "oid", "pid", "cvl", cut=11)

result    = container.SyncSCell(cell, flag_capture_delta=True)
check     = (result.code           == CODES_COMPLETION.COMPLETED)
check    &= (result.data.cut       == 11)
print(f"{'[+]' if check else '[ ]'} Синхронизация обновлённой S-Ячейки")

cell      = T20_StructCell("oci", "oid", "pid", "", cut=0)

result    = container.ReadSCell(cell)
check     = (result.code           == CODES_COMPLETION.COMPLETED)
check    &= (result.data           == T20_StructCell("oci", "oid", "pid", "cvl", cut=11))
print(f"{'[+]' if check else '[ ]'} Сверка S-Ячейки")
