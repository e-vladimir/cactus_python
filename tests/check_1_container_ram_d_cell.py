# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-RAM
# 24 окт 2024

import time

import pytest

from G00_status_codes         import *
from G20_cactus_struct        import T20_StructCell
from G31_cactus_container_ram import C31_ContainerRAM

print("")
print("[== Тест Контейнера-RAM: D-Ячейка ==]")
@pytest.mark.default
@pytest.mark.ram
def test_container_ram_d_cell():
    container  = C31_ContainerRAM()

    cell_wrong = T20_StructCell(idc="idc",            idp="idp", vlp="???", vlt=20)
    cell       = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="???", vlt=20)

    time_0 = time.time()
    result = container.ReadDCell(cell_wrong)
    time_1 = time.time()
    check  = result.code == CODES_COMPLETION.INTERRUPTED
    check &= CODES_DATA.ERROR_CHECK in result.subcodes
    print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение некорректной ячейки")
    if not check: print(f"                  {result.code} {result.subcodes}\n")
    assert check

    time_0 = time.time()
    result = container.ReadDCell(cell)
    time_1 = time.time()
    check  = result.code == CODES_COMPLETION.INTERRUPTED
    check &= CODES_DATA.NO_DATA in result.subcodes
    print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение из пустого контейнера")
    if not check: print(f"                  {result.code} {result.subcodes}\n")
    assert check

    time_0 = time.time()
    result = container.DeleteSCell(cell)
    time_1 = time.time()
    check  = result.code == CODES_COMPLETION.COMPLETED
    check &= CODES_DATA.NO_DATA in result.subcodes
    print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление без захвата изменений")
    if not check: print(f"                  {result.code} {result.subcodes}\n")
    assert check

    time_0 = time.time()
    result = container.DeleteSCell(cell, flag_capture_delta=True)
    time_1 = time.time()
    check  = result.code == CODES_COMPLETION.COMPLETED
    check &= CODES_DATA.NO_DATA in result.subcodes
    print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление с захватом изменений")
    if not check: print(f"                  {result.code} {result.subcodes}\n")
    assert check

    time_0 = time.time()
    result = container.WriteDCell(cell)
    time_1 = time.time()
    result = container.ReadDCell(cell)
    check  = result.code == CODES_COMPLETION.COMPLETED
    print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Запись без захвата изменений")
    if not check: print(f"                  {result.code} {result.subcodes}\n")
    assert check

    time_0 = time.time()
    result = container.DeleteDCell(cell, flag_capture_delta=True)
    time_1 = time.time()
    check  = result.code == CODES_COMPLETION.COMPLETED
    check &= result.data == cell
    print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Удаление c захватом изменений")
    if not check: print(f"                  {result.code} {result.subcodes}\n")
    assert check

    time_0 = time.time()
    result = container.WriteDCell(cell, flag_capture_delta=True)
    time_1 = time.time()
    check  = result.code == CODES_COMPLETION.COMPLETED
    check &= result.data == cell
    print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Запись с захватом изменений")
    if not check: print(f"                  {result.code} {result.subcodes}\n")
    assert check

    time_0 = time.time()
    result = container.WriteDCell(cell, flag_capture_delta=True)
    time_1 = time.time()
    check  = result.code == CODES_COMPLETION.COMPLETED
    check &= CODES_PROCESSING.SKIP in result.subcodes
    print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Пропуск при перезаписи")
    if not check: print(f"                  {result.code} {result.subcodes}\n")
    assert check

    time_0 = time.time()
    result = container.ReadDCell(cell)
    time_1 = time.time()
    check  = result.code == CODES_COMPLETION.COMPLETED
    check &= result.data == cell
    print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение")
    if not check: print(f"                  {result.code} {result.subcodes}\n")
    assert check
