import random

from G20_cactus_struct import T20_StructCell
from G21_struct_result import T21_StructRange
from G30_cactus_controller_containers import controller_containers

count = 100

print("Тест SQLite-Контейнера: Работа с D-Ячейками")
print("")

container = controller_containers.RegisterContainerSQLite("sqlite")
container.OptionsFilename("./data.sqlite")
container.Connect()

oci    = "class_01"
container.RegisterClass(oci)
container.DeleteDCells(T21_StructRange(oci=oci))

result = len(container.ReadDCells(T21_StructRange(oci=oci)).cells) == 0
print(f"{'[+]' if result else '[ ]'} Проверка удаления всех D-Ячеек")

oci        = "class_01"
oid        = "object-01"
cells      = []

for index in range(count):
	pid    = f"field-{random.randint(0, count)}"
	cvl    = f"value-{random.randint(0, count)}"
	cut    = random.randint(0, 100000)
	cell   = T20_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
	cells.append(cell)

container.WriteDCells(cells)
result = len(container.ReadDCells(T21_StructRange(oci=oci)).cells) == count
print(f"{'[+]' if result else '[ ]'} Проверка записи {count} D-Ячеек")

container.DeleteDCells(T21_StructRange(oci=oci))
result = len(container.ReadDCells(T21_StructRange(oci=oci)).cells) == 0
print(f"{'[+]' if result else '[ ]'} Проверка удаления всех D-Ячеек")
