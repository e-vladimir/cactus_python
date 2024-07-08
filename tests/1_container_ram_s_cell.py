# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-RAM
# 08 июл 2024

from G20_cactus_struct        import T20_StructCell
from G31_cactus_container_ram import C31_ContainerRAM

print("")
print("[== Тест Контейнера-RAM: S-Ячейка ==]")

container = C31_ContainerRAM()

cell = T20_StructCell(idc="idc", ido="ido", idp="idp", vlp="", vlt=0)

result = container.ReadSCell(cell)
print(result)

result = container.DeleteSCell(cell)
print(result)
