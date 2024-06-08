from G30_cactus_controller_containers import controller_containers
from G20_cactus_struct import T20_StructCell

print("Тест SQLite-Контейнера: Работа с пакетами S-Ячеек")
print("")

container = controller_containers.RegisterContainerSQLite("sqlite")
container.OptionsFilename("./data.sqlite")
container.Connect()

oci    = "class_01"
container.RegisterClass(oci)

cell   = T20_StructCell(oci=oci)
container.DeleteSCells(cell)

result = len(container.ReadSCells(cell).cells) == 0
print(f"{'[+]' if result else '[ ]'} Подготовка контейнера")

oci        = "class_01"
oid        = "object-01"
cells      = []

for index in range(0, 100):
	pid    = f"field-{index}"
	cvl    = f"value-{index}"
	cut    = 1
	cell   = T20_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
	cells.append(cell)

container.WriteSCells(cells)

cell   = T20_StructCell(oci=oci)
result = len(container.ReadSCells(cell).cells) == 100
print(f"{'[+]' if result else '[ ]'} Запись 100 S-Ячеек")

container.DeleteSCells(cell)
result = len(container.ReadSCells(cell).cells) == 0
print(f"{'[+]' if result else '[ ]'} Удаление S-Ячеек")

oci        = "class_01"
oid        = "object-01"
cells      = []

for index in range(1, 11):
	pid    = f"field-{index}"
	cvl    = f"value-{index}"
	cut    = 1
	cell   = T20_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
	cells.append(cell)

result = len(container.WriteSCells(cells).cells) == 10
print(f"{'[+]' if result else '[ ]'} Запись 10 S-Ячеек")

oci        = "class_01"
oid        = "object-01"
cells      = []

for index in range(6, 16):
	pid    = f"field-{index}"
	cvl    = f"value-{index}"
	cut    = 1
	cell   = T20_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
	cells.append(cell)

deleted_cells = container.DeleteSCells(cells)
result        = len(deleted_cells.cells) == 5
print(f"{'[+]' if result else '[ ]'} Удаление 5 + 5 S-Ячеек")
