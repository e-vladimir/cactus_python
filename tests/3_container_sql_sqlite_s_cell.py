# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-SQL: SQLite
# 16 июн 2024

import os

from G00_status_codes         import *

from G20_cactus_struct        import T20_StructCell
from G32_cactus_container_sql import C32_ContainerSQLite

print("")
print("[== Тест Контейнера-SQL-SQLite: S-Ячейка ==]")

try   : os.remove("./data.sqlite")
except: pass

container = C32_ContainerSQLite()
container.OptionsFilename("./data.sqlite")
container.ConnectMode_Auto(True)

cell      = T20_StructCell("oci", "oid", "pid",   "cvl",     0)
cell_new  = T20_StructCell("oci", "oid", "pid",   "cvl-10", 10)
cell_1    = T20_StructCell("oci", "oid", "pid-1", "cvl-1",   1)
cell_2    = T20_StructCell("oci", "oid", "pid-2", "cvl-2",   2)

result    = container.RegisterClass("oci")
check     = (result.code        == CODES_COMPLETION.COMPLETED)
print(f"{'[+]' if check else '[ ]'} Регистрация класса OCI")

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
print(f"{'[+]' if check else '[ ]'} Запись S-Ячейки без пропуска и без захвата изменений")

result    = container.DeleteSCell(cell)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        is None)
print(f"{'[+]' if check else '[ ]'} Удаление S-Ячейки без захвата изменений")

result    = container.WriteSCell(cell, flag_skip=False, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        == cell)
print(f"{'[+]' if check else '[ ]'} Запись S-Ячейки без пропуска и с захватом изменений")

result    = container.DeleteSCell(cell, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        == cell)
print(f"{'[+]' if check else '[ ]'} Удаление S-Ячейки с захватом изменений")

result    = container.WriteSCell(cell, flag_skip=True, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        == cell)
print(f"{'[+]' if check else '[ ]'} Запись S-Ячейки с пропуском и с захватом изменений")

result    = container.WriteSCell(cell, flag_skip=True, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (CODES_PROCESSING.SKIP in result.subcodes)
check    &= (result.data        is None)
print(f"{'[+]' if check else '[ ]'} Пропуск записи S-Ячейки с пропуском и с захватом изменений")

result    = container.DeleteSCell(cell, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        == cell)
print(f"{'[+]' if check else '[ ]'} Удаление S-Ячейки с захватом изменений")

result    = container.WriteSCell(cell, flag_skip=True, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        == cell)
print(f"{'[+]' if check else '[ ]'} Запись S-Ячейки #0")

result    = container.WriteSCell(cell_1, flag_skip=True, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        == cell_1)
print(f"{'[+]' if check else '[ ]'} Запись S-Ячейки #1")

result    = container.WriteSCell(cell_2, flag_skip=True, flag_capture_delta=True)
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= (result.data        == cell_2)
print(f"{'[+]' if check else '[ ]'} Запись S-Ячейки #2")

result    = container.ReadSCell(T20_StructCell("oci", "oid", "pid"))
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (result.data == cell)
print(f"{'[+]' if check else '[ ]'} Чтение S-Ячейки #0")

result    = container.ReadSCell(T20_StructCell("oci", "oid-1", "pid"))
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (CODES_PROCESSING.SKIP in result.subcodes)
check    &= (CODES_DATA.NO_DATA    in result.subcodes)
check    &= (result.data is None)
print(f"{'[+]' if check else '[ ]'} Чтение неизвестной S-Ячейки")

result    = container.SyncSCell(cell, flag_capture_delta=True)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (CODES_PROCESSING.SKIP in result.subcodes)
check    &= (result.data == cell)
print(f"{'[+]' if check else '[ ]'} Пропуск синхронизации S-Ячейки #0")

result    = container.SyncSCell(cell_new, flag_capture_delta=True)
check     = (result.code == CODES_COMPLETION.COMPLETED)
check    &= (result.data == cell_new)
print(f"{'[+]' if check else '[ ]'} Синхронизация S-Ячейки до #10")
