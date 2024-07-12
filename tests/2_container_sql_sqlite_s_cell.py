# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-SQL.SQLite
# 12 июл 2024

import os
import time

from G00_status_codes         import *

from G20_cactus_struct        import T20_StructCell

from G32_cactus_container_sql import C32_ContainerSQLite

print("")
print("[== Тест Контейнера-SQL.SQLite: S-Ячейка ==]")

try   : os.remove("./data.sqlite")
except: pass

container = C32_ContainerSQLite()
container.OptionsFilename("./data.sqlite")
container.Connect()

cell = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="???", vlt=20)

time_0 = time.time()
result = container.RegisterClass(cell.idc)
check  = result.code == CODES_COMPLETION.COMPLETED
time_1 = time.time()
print("[+]" if check else "[ ]", f"Регистрация класса ({(time_1 - time_0):0.3f} сек)")

time_0 = time.time()
result = container.ReadSCell(cell)
check  = result.code == CODES_COMPLETION.INTERRUPTED
check &= CODES_DATA.NO_DATA in result.subcodes
time_1 = time.time()
print("[+]" if check else "[ ]", f"Чтение из пустого контейнера ({(time_1 - time_0):0.3f} сек)")

time_0 = time.time()
result = container.DeleteSCell(cell)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
time_1 = time.time()
print("[+]" if check else "[ ]", f"Удаление без захвата изменений ({(time_1 - time_0):0.3f} сек)")

time_0 = time.time()
result = container.DeleteSCell(cell, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
time_1 = time.time()
print("[+]" if check else "[ ]", f"Удаление с захватом изменений ({(time_1 - time_0):0.3f} сек)")

time_0 = time.time()
result = container.WriteSCell(cell, flag_skip=False, flag_capture_delta=False)
check  = result.code == CODES_COMPLETION.COMPLETED
time_1 = time.time()
print("[+]" if check else "[ ]", f"Запись без захвата изменений ({(time_1 - time_0):0.3f} сек)")

time_0 = time.time()
result = container.WriteSCell(cell, flag_skip=False, flag_capture_delta=False)
check  = result.code == CODES_COMPLETION.COMPLETED
time_1 = time.time()
print("[+]" if check else "[ ]", f"Перезапись без захвата изменений ({(time_1 - time_0):0.3f} сек)")

time_0 = time.time()
result = container.WriteSCell(cell, flag_skip=True, flag_capture_delta=False)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_PROCESSING.SKIP in result.subcodes
time_1 = time.time()
print("[+]" if check else "[ ]", f"Пропуск записи без захвата изменений ({(time_1 - time_0):0.3f} сек)")

time_0 = time.time()
result = container.DeleteSCell(cell, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
time_1 = time.time()
print("[+]" if check else "[ ]", f"Удаление c захватом изменений ({(time_1 - time_0):0.3f} сек)")

time_0 = time.time()
result = container.WriteSCell(cell, flag_skip=False, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
time_1 = time.time()
print("[+]" if check else "[ ]", f"Запись с захватом изменений ({(time_1 - time_0):0.3f} сек)")

cell = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="???", vlt=21)

time_0 = time.time()
result = container.WriteSCell(cell, flag_skip=False, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
time_1 = time.time()
print("[+]" if check else "[ ]", f"Перезапись c захватом изменений ({(time_1 - time_0):0.3f} сек)")

time_0 = time.time()
result = container.WriteSCell(cell, flag_skip=True, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_PROCESSING.SKIP in result.subcodes
check &= result.data is None
time_1 = time.time()
print("[+]" if check else "[ ]", f"Пропуск записи с захватом изменений ({(time_1 - time_0):0.3f} сек)")

time_0 = time.time()
result = container.ReadSCell(cell)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
time_1 = time.time()
print("[+]" if check else "[ ]", f"Чтение ({(time_1 - time_0):0.3f} сек)")

cell = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="???", vlt=22)

time_0 = time.time()
result = container.SyncSCell(cell, flag_capture_delta=False)
check  = result.code == CODES_COMPLETION.COMPLETED
time_1 = time.time()
print("[+]" if check else "[ ]", f"Синхронизация ячейки (обновление) без захвата изменений ({(time_1 - time_0):0.3f} сек)")

cell = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="???", vlt=25)

time_0 = time.time()
result = container.SyncSCell(cell, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check  = result.data == cell
time_1 = time.time()
print("[+]" if check else "[ ]", f"Синхронизация ячейки (обновление) с захватом изменений ({(time_1 - time_0):0.3f} сек)")

cell = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="???", vlt=20)

time_0 = time.time()
result = container.SyncSCell(cell, flag_capture_delta=False)
check  = result.code == CODES_COMPLETION.COMPLETED
time_1 = time.time()
print("[+]" if check else "[ ]", f"Синхронизация ячейки (пропуск) без захвата изменений ({(time_1 - time_0):0.3f} сек)")

time_0 = time.time()
result = container.SyncSCell(cell, flag_capture_delta=True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_PROCESSING.SKIP in result.subcodes
check  = result.data.vlt == 25
time_1 = time.time()
print("[+]" if check else "[ ]", f"Синхронизация ячейки (пропуск) с захватом изменений ({(time_1 - time_0):0.3f} сек)")
