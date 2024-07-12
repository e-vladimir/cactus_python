# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-RAM
# 12 июл 2024

import os

from G00_status_codes         import *

from G20_cactus_struct        import T20_StructCell

from G32_cactus_container_sql import C32_ContainerSQLite

print("")
print("[== Тест Контейнера-RAM: Пакет S-Ячеек ==]")

try   : os.remove("./data.sqlite")
except: pass

container = C32_ContainerSQLite()
container.OptionsFilename("./data.sqlite")
container.Connect()

cell = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="???", vlt=20)

result = container.RegisterClass(cell.idc)
check  = result.code == CODES_COMPLETION.COMPLETED
print("[+]" if check else "[ ]", "Регистрация класса")

cell  =  T20_StructCell(idc="idc", ido="ido")
cells = [T20_StructCell(idc="idc", ido="ido", idp=f"idp_{index}", vlp=f"value_{index}") for index in range(10)]

result = container.ReadSCells(cell)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Чтение по маске из пустого контейнера")

result = container.ReadSCells(cells)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Чтение по списку из пустого контейнера")

result = container.DeleteSCells(cell, False, False)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Удаление по маске из пустого контейнера без захвата изменений в последовательном режиме")

result = container.DeleteSCells(cell, True, False)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Удаление по маске из пустого контейнера без захвата изменений в пакетном режиме")

result = container.DeleteSCells(cell, True, True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Удаление по маске из пустого контейнера c захватом изменений в пакетном режиме")

result = container.DeleteSCells(cell, False, True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Удаление по маске из пустого контейнера c захватом изменений в последовательном режиме")

result = container.DeleteSCells(cells, False, False)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Удаление по списку из пустого контейнера без захвата изменений в последовательном режиме")

result = container.DeleteSCells(cells, True, False)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Удаление по списку из пустого контейнера без захвата изменений в пакетном режиме")

result = container.DeleteSCells(cells, True, True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Удаление по списку из пустого контейнера c захватом изменений в пакетном режиме")

result = container.DeleteSCells(cells, False, True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Удаление по списку из пустого контейнера c захватом изменений в последовательном режиме")

result = container.WriteSCells(cells, False, False, False)
check  = result.code == CODES_COMPLETION.COMPLETED
print("[+]" if check else "[ ]", "Запись ячеек без захвата изменений в последовательном режиме")

result = container.ReadSCells(cell)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == 10
print("[+]" if check else "[ ]", "Чтение по маске")

result = container.ReadSCells(cells)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == 10
print("[+]" if check else "[ ]", "Чтение по списку")

result = container.DeleteSCells(cell, False, False)
check  = result.code == CODES_COMPLETION.COMPLETED
print("[+]" if check else "[ ]", "Удаление по маске без захвата изменений в последовательном режиме")

result = container.WriteSCells(cells, False, False, True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == 10
print("[+]" if check else "[ ]", "Запись ячеек c захватом изменений в последовательном режиме")

result = container.DeleteSCells(cell, False, True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == 10
print("[+]" if check else "[ ]", "Удаление по маске c захватом изменений в последовательном режиме")

result = container.WriteSCells(cells, False, False, False)
result = container.WriteSCells(cells, False, False, True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Перезапись ячеек c захватом изменений в последовательном режиме")

result = container.WriteSCells(cells, False, True, True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print("[+]" if check else "[ ]", "Пропуск записи ячеек c захватом изменений в последовательном режиме")

result = container.DeleteSCells(cell, True, True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == 10
print("[+]" if check else "[ ]", "Удаление по маске c захватом изменений в пакетном режиме")

result = container.WriteSCells(cells, True, True, True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == 10
print("[+]" if check else "[ ]", "Запись ячеек c захватом изменений в пакетном режиме")

result = container.DeleteSCells(cells, False, True)
check  = result.code == CODES_COMPLETION.COMPLETED
check &= len(result.data) == 10
print("[+]" if check else "[ ]", "Удаление по списку c захватом изменений в последовательном режиме")
