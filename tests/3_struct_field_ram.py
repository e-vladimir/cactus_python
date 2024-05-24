import datetime

from G00_result_codes                 import RESULT_OK
from G30_cactus_controller_containers import controller_containers
from G30_cactus_frame                 import C30_StructFrame, C30_StructField

print("Тест структурного параметра: Общая проверка с контейнером RAM")
print("")


class C40_Book(C30_StructFrame):
	_oci = "Книга"

	def InitFields(self):
		self.f_name    = C30_StructField(self, "Наименование",   "Неизвестно")
		self.f_year    = C30_StructField(self, "Год издания",     1900)
		self.f_author  = C30_StructField(self, "Автор",          "Неизвестно")
		self.f_reprint = C30_StructField(self, "Года переиздания")
		self.f_price   = C30_StructField(self, "Стоимость",       0)


book      = C40_Book("Книга 1")
container = controller_containers.RegisterContainerRAM("RAM")

book_name     = "Поваренная книга"
book_year     = 0
book_author   = "Жуй деПлюй"
book_reprints = [1900, 1901, 1902, 1904]

result = book.f_author.Pid().text == "Автор"
print(f"{'[+]' if result else '[ ]'} Проверка PID")

result = book.f_name.Sid().text == f"{book.Oid().text}.{book.f_name.Pid().text}"
print(f"{'[+]' if result else '[ ]'} Проверка SID")

result = book.f_name.Cid().text == f"{book.Oci().text}.{book.Oid().text}.{book.f_name.Pid().text}"
print(f"{'[+]' if result else '[ ]'} Проверка CID")

result = book.f_name.ToString("RAM").text == "Неизвестно"
print(f"{'[+]' if result else '[ ]'} Чтение текстового значения параметра по-умолчанию")

book.f_name.DefaultCvl(book_author)
result = book.f_name.ToString("RAM").text == book_author
print(f"{'[+]' if result else '[ ]'} Проверка установки текстового значения параметра по-умолчанию")

result = book.f_name.FromString("RAM", book_name).code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Запись текстового значения параметра в контейнер")

result = book.f_name.ToString("RAM").text == book_name
print(f"{'[+]' if result else '[ ]'} Чтение текстового значения параметра из контейнера")

book.f_year.FromString("RAM", "0")
result = book.f_year.ToString("RAM").text == "0"
print(f"{'[+]' if result else '[ ]'} Конвертация из/в строки")

book.f_year.FromInteger("RAM", 1)
result = book.f_year.ToInteger("RAM").value == 1
print(f"{'[+]' if result else '[ ]'} Конвертация из/в целого числа")

book.f_year.FromFloat("RAM", 2.0)
result = book.f_year.ToFloat("RAM").value == 2.0
print(f"{'[+]' if result else '[ ]'} Конвертация из/в дробного числа")

book.f_year.FromBoolean("RAM", False)
result = not book.f_year.ToBoolean("RAM").flag
print(f"{'[+]' if result else '[ ]'} Конвертация из/в логического значения")

dtime_sys = datetime.datetime.now()
book.f_year.FromDatetime("RAM", dtime_sys)

dtime_ram = book.f_year.ToDatetime("RAM").dtime
result = True
result = result and dtime_ram.year   == dtime_sys.year
result = result and dtime_ram.month  == dtime_sys.month
result = result and dtime_ram.day    == dtime_sys.day
result = result and dtime_ram.hour   == dtime_sys.hour
result = result and dtime_ram.minute == dtime_sys.minute
result = result and dtime_ram.second == dtime_sys.second
print(f"{'[+]' if result else '[ ]'} Конвертация из даты/времени")

result = not book.f_name.ToDatetime("RAM").code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Проверка отказа преобразования в дату/время")

result = not book.f_name.ToInteger("RAM").code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Проверка отказа преобразования в целое число")

result = not book.f_name.ToFloat("RAM").code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Проверка отказа преобразования в дробное число")

result = not book.f_name.ToBoolean("RAM").flag
print(f"{'[+]' if result else '[ ]'} Проверка отказа преобразования в логическое значение")

book.f_reprint.FromStrings("RAM", list(map(str, book_reprints)))
result = book.f_reprint.ToStrings("RAM").items == list(map(str, book_reprints))
print(f"{'[+]' if result else '[ ]'} Конвертация из/в списка строк")

book.f_reprint.FromIntegers("RAM", book_reprints)
result = book.f_reprint.ToIntegers("RAM").items == book_reprints
print(f"{'[+]' if result else '[ ]'} Конвертация из/в списка целых чисел")

book.f_reprint.FromFloats("RAM", list(map(float, book_reprints)))
result = book.f_reprint.ToFloats("RAM").items == list(map(float, book_reprints))
print(f"{'[+]' if result else '[ ]'} Конвертация из/в списка дробных чисел")

values = [True, False, True, False, True]
book.f_reprint.FromBooleans("RAM", values)
result = book.f_reprint.ToBooleans("RAM").items == values
print(f"{'[+]' if result else '[ ]'} Конвертация из/в списка логических значений")

values = []
for index in range(10): values.append(datetime.datetime(year=1900, month=1, day=1, hour=index, minute=0, second=0))
book.f_reprint.FromDatetimes("RAM", values)
result = book.f_reprint.ToDatetimes("RAM").items == values
print(f"{'[+]' if result else '[ ]'} Конвертация из/в списка даты/времени")

utime = int(datetime.datetime.now().timestamp())
book.f_name.FromString("RAM", "О полезных существах")
result = book.f_name.Cut("RAM").value == utime
print(f"{'[+]' if result else '[ ]'} Запрос CUT")

book.DeleteObject("RAM")
result = len(container._s_cells) == 0
print(f"{'[+]' if result else '[ ]'} Удаление объекта из контейнера")

cut = 1000

result = book.f_price.WriteCvl("RAM", "1000", 1000).code == RESULT_OK
result = result and len(container._d_cells[book.f_price.Sid().text].items()) == 1
print(f"{'[+]' if result else '[ ]'} Добавление записи D-Данных")

result = book.f_price.ReadCvl("RAM", 1000).code == RESULT_OK
result = result and book.f_price.ReadCvl("RAM", 1000).text == "1000"
print(f"{'[+]' if result else '[ ]'} Запрос записи D-Данных")

result = book.f_price.ReadCvl("RAM").code == RESULT_OK
result = result and book.f_price.ReadCvl("RAM").text == "1000"
print(f"{'[+]' if result else '[ ]'} Запрос последней записи D-Данных")

for cut in range(10, 1001, 10):	book.f_price.WriteCvl("RAM",  f"{cut}", cut)

result_range = book.f_price.CutRange("RAM")
result = result_range.code == RESULT_OK
result = result and result_range.cut_l == 10
result = result and result_range.cut_r == 1000
print(f"{'[+]' if result else '[ ]'} Запрос границ cut D-Данных")

result_cuts = book.f_price.Cuts("RAM", 10, 50)
result = result_cuts.code == RESULT_OK
cuts = result_cuts.items
cuts.sort()
result = result and cuts == [10, 20, 30, 40, 50]
print(f"{'[+]' if result else '[ ]'} Запрос списка cut в диапазоне cut D-Данных")

result_cvls = book.f_price.Cvls("RAM", 10, 50)
result = result_cvls.code == RESULT_OK
cvls = result_cvls.items

result = result and cvls == {10: "10", 20 : "20", 30 : "30", 40 : "40", 50 : "50"}
print(f"{'[+]' if result else '[ ]'} Запрос списка cut в диапазоне cut D-Данных")
