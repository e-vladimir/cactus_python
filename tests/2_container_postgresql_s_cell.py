from G00_result_codes                 import RESULT_OK, RESULT_WARNING_NO_DATA
from G30_cactus_controller_containers import controller_containers
from G20_cactus_struct import T20_StructCell

print("Тест PostgreSQL-Контейнера: Работа с S-Ячейкой")
print("")

container = controller_containers.RegisterContainerPostgreSQL("postgresql")
container.OptionsServerIp("195.161.41.96")
container.OptionsServerTcpPort(5432)
container.OptionsServerDBase("fin_sync")
container.OptionsServerLogin("a6540920979")
container.OptionsServerPassword('!-dg7/X"0c@JqSOd')
container.Connect()

oci    = "class_01"
container.RegisterClass(oci)

container.DeleteSCells(T20_StructCell(oci=oci))

oid    = "object-01"
pid    = "field-01"
cvl    = "value-01"
cut    = 0
cell   = T20_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
result = container.WriteSCell(cell).code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Запись S-Ячейки")

cell   = T20_StructCell(oci=oci, oid=oid, pid=pid)
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
cell   = T20_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
container.WriteSCell(cell)
cell   = T20_StructCell(oci=oci, oid=oid, pid=pid)
cell   = container.ReadSCell(cell).cell
result = True
if   not cell.oci == oci: result = False
elif not cell.oid == oid: result = False
elif not cell.pid == pid: result = False
elif not cell.cvl == cvl: result = False
elif not cell.cut == cut: result = False
print(f"{'[+]' if result else '[ ]'} Перезапись S-Ячейки (режим перезаписи)")

oid    = "object-01"
pid    = "field-01"
cvl    = "value-03"
cut    = 2
cell   = T20_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
container.WriteSCell(cell, True)
cvl    = "value-02"
cut    = 1
cell   = T20_StructCell(oci=oci, oid=oid, pid=pid)
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
cell   = T20_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
container.SyncSCell(cell)
cell   = T20_StructCell(oci=oci, oid=oid, pid=pid)
cell   = container.ReadSCell(cell).cell
result = True
if   not cell.oci == oci: result = False
elif not cell.oid == oid: result = False
elif not cell.pid == pid: result = False
elif not cell.cvl == cvl: result = False
elif not cell.cut == cut: result = False
print(f"{'[+]' if result else '[ ]'} Синхронизация S-Ячейки")

oid    = "object-01"
pid    = "field-01"
cell   = T20_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
container.DeleteSCell(cell)
result = container.ReadSCell(cell).code == RESULT_WARNING_NO_DATA
print(f"{'[+]' if result else '[ ]'} Удаление S-Ячейки")

cell   = T20_StructCell(oci=oci)
container.DeleteSCells(cell)
result = container.ReadSCells(cell).code == RESULT_WARNING_NO_DATA
print(f"{'[+]' if result else '[ ]'} Удаление всех S-Ячеек")

container.Disconnect()
