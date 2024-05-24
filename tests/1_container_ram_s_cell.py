from G00_result_codes                 import RESULT_OK
from G30_cactus_struct                import T30_StructCell
from G30_cactus_controller_containers import controller_containers

print("Тест RAM-Контейнера: Работа с S-Ячейкой")
print("")

container = controller_containers.RegisterContainerRAM("RAM")

oci    = "class_01"
oid    = "object-01"
pid    = "field-01"
cvl    = "value-01"
cut    = 0
cell   = T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
result = container.WriteSCell(cell).code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Запись S-Ячейки")

cell   = T30_StructCell(oci=oci, oid=oid, pid=pid)
cell   = container.ReadSCell(cell).cell
result = True
if   not cell.oci == oci: result = False
elif not cell.oid == oid: result = False
elif not cell.pid == pid: result = False
elif not cell.cvl == cvl: result = False
elif not cell.cut == cut: result = False
print(f"{'[+]' if result else '[ ]'} Чтение S-Ячейки")

cvl    = "value-02"
cut    = 1
cell   = T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
container.WriteSCell(cell)
cell   = T30_StructCell(oci=oci, oid=oid, pid=pid)
cell   = container.ReadSCell(cell).cell
result = True
if   not cell.oci == oci: result = False
elif not cell.oid == oid: result = False
elif not cell.pid == pid: result = False
elif not cell.cvl == cvl: result = False
elif not cell.cut == cut: result = False
print(f"{'[+]' if result else '[ ]'} Перезапись S-Ячейки (режим перезаписи)")

oci    = "class_01"
oid    = "object-01"
pid    = "field-01"
cvl    = "value-03"
cut    = 2
cell   = T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
container.WriteSCell(cell, True)
cvl    = "value-02"
cut    = 1
cell   = T30_StructCell(oci=oci, oid=oid, pid=pid)
cell   = container.ReadSCell(cell).cell
result = True
if   not cell.oci == oci: result = False
elif not cell.oid == oid: result = False
elif not cell.pid == pid: result = False
elif not cell.cvl == cvl: result = False
elif not cell.cut == cut: result = False
print(f"{'[+]' if result else '[ ]'} Перезапись S-Ячейки (режим пропуска данных)")

cvl    = "value-10"
cut    = 10
cell   = T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
container.SyncSCell(cell)
cell   = T30_StructCell(oci=oci, oid=oid, pid=pid)
cell   = container.ReadSCell(cell).cell
result = True
if   not cell.oci == oci: result = False
elif not cell.oid == oid: result = False
elif not cell.pid == pid: result = False
elif not cell.cvl == cvl: result = False
elif not cell.cut == cut: result = False
print(f"{'[+]' if result else '[ ]'} Синхронизация S-Ячейки")

oci    = "class_01"
oid    = "object-01"
pid    = "field-01"
cell   = T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
container.DeleteSCell(cell)
result = len(container._s_cells) == 0
print(f"{'[+]' if result else '[ ]'} Удаление S-Ячейки")
