# ТЕСТ РАБОТЫ С ОБЪЕКТАМИ

from G10_list_extended                import DistinctAndNatSortList1D
from G30_cactus_controller_containers import controller_containers
from G30_cactus_datafilters           import C30_FilterLinear1D
from G30_cactus_frame                 import C30_StructField
from G31_cactus_frame                 import C31_StructFrameWithEvents

CONTAINER = "SQLite"


class Note(C31_StructFrameWithEvents):
	_idc = "Заметка"

	def Init_10(self):
		super().Init_10()

		self.title = C30_StructField(self, "Заголовок")
		self.text  = C30_StructField(self, "Текст")

	def Title(self, title: str = None) -> str:
		if title is None: return self.title.ToString(CONTAINER).data
		else            :        self.title.FromString(CONTAINER, title)

	def Text(self, text: str = None) -> str:
		if text is None: return self.text.ToString(CONTAINER).data
		else           :        self.text.FromString(CONTAINER, text)

	def __str__(self):
		return f"{self.Title()} - {self.Text()}"


def CreateNote(title: str, text: str):
	note = Note()
	note.GenerateIdo()
	note.Title(title)
	note.Text(text)

	return note.Ido().data


def DeleteNote(ido: str):
	note = Note(ido)
	note.DeleteObject(CONTAINER)


def GetNoteIdo(title: str):
	note = Note()
	idc      : str = note.Idc().data
	idp_title: str = note.title.Idp().data

	filter_notes   = C30_FilterLinear1D(idc)
	filter_notes.FilterIdpVlpByEqual(idp_title, title)
	filter_notes.Capture(CONTAINER)

	idos           = filter_notes.Idos().data

	if not idos: return None
	return idos[0]


def GetNoteIdos():
	return Note.Idos(CONTAINER).data


def PrintNoteIdos(idos: list[str]):
	notes : list[str] = []
	for ido in idos:
		notes.append(Note(ido).__str__())
	notes_sorted = DistinctAndNatSortList1D(notes, flag_sort = True)
	print(notes_sorted, end="\n\n")


container = controller_containers.RegisterContainerSQLite(CONTAINER)
container.OptionsFilename("my_data")
container.Connect()

Note.RegisterClass(CONTAINER)

print("До добавления заметок: ")
PrintNoteIdos(GetNoteIdos())

# ido_1 = CreateNote("Заголовок 1", "Текст 1")
# ido_2 = CreateNote("Заголовок 2", "Текст 2")
# ido_3 = CreateNote("Заголовок 3", "Текст 3")
#
# print("После добавления заметок: ")
# PrintNoteIdos(GetNoteIdos())
#
# ido_4 = GetNoteIdo("qwerty")
# ido_5 = GetNoteIdo("Заголовок 2")
#
# print("ido_1:", Note(ido_1))
# print("ido_2:", Note(ido_2))
# print("ido_3:", Note(ido_3))
# print("ido_4:", Note(ido_4))
# print("ido_5:", Note(ido_5), end="\n\n")
#
# DeleteNote(ido_4)
# DeleteNote(ido_5)
#
# print("После удаления заметок: ")
# PrintNoteIdos(GetNoteIdos())
