# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-SQL.SQLite
# 12 июл 2024

import os
import time

from G00_status_codes         import *

from G20_cactus_struct        import T20_StructCell

from G32_cactus_container_sql import C32_ContainerSQLite

print("")
print("[== Тест Контейнера-SQL.SQLite: D-Ячейка ==]")

try   : os.remove("./data.sqlite")
except: pass

container = C32_ContainerSQLite()
container.OptionsFilename("./data.sqlite")
container.Connect()

cell       = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="???", vlt=0)
cell_wrong = T20_StructCell(idc="idc",            idp="idp", vlp="???", vlt=0)

time_0 = time.time()
result = container.RegisterClass(cell.idc)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Регистрация класса")

cell_wrong = T20_StructCell(idc="idc",            idp="idp", vlp="???", vlt=20)
cell       = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="???", vlt=20)

time_0 = time.time()
result = container.ReadDCell(cell_wrong)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.INTERRUPTED
check &= CODES_DATA.ERROR_CHECK in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "Чтение некорректной ячейки")

time_0 = time.time()
result = container.ReadDCell(cell)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.INTERRUPTED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "Чтение из пустого контейнера")

time_0 = time.time()
result = container.DeleteSCell(cell)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "Удаление без захвата изменений")

time_0 = time.time()
result = container.DeleteSCell(cell, flag_capture_delta=True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "Удаление с захватом изменений")

time_0 = time.time()
result = container.WriteDCell(cell)
time_1 = time.time()
result = container.ReadDCell(cell)
check  = result.code == CODES_COMPLETION.COMPLETED
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "Запись без захвата изменений")

time_0 = time.time()
result = container.DeleteDCell(cell, flag_capture_delta=True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "Удаление c захватом изменений")

time_0 = time.time()
result = container.WriteDCell(cell, flag_capture_delta=True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "Запись с захватом изменений")

time_0 = time.time()
result = container.WriteDCell(cell, flag_capture_delta=True)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_PROCESSING.SKIP in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "Пропуск при перезаписи")

time_0 = time.time()
result = container.ReadDCell(cell)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= result.data == cell
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "Чтение")
