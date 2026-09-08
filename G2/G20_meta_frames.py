# МЕТА-КАРКАСЫ
# 08 сен 2026


class C20_MetaFrame:
	"""  Мета-каркас"""
	
	def __init__(self):
		self.Init_00()
		self.Init_01()
		self.Init_10()
		self.Init_11()
		self.Init_12()
		self.Init_20()
		
		self.onInited()

	def Init_00(self):
		""" Инициализация параметров """
		pass

	def Init_01(self):
		""" Настройка параметров """
		pass

	def Init_10(self):
		""" Инициализация объектов """
		pass

	def Init_11(self):
		""" Настройка объектов """
		pass

	def Init_12(self):
		""" Обработчик объектов """
		pass

	def Init_20(self):
		""" Внутренний обработчик """
		pass

	# События
	def onInited(self): pass


class C20_MetaSingletonFrame(type):
	""" Мета-singleton для применения через параметр metaclass """

	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances: cls._instances[cls] = super().__call__(*args, **kwargs)
		return cls._instances[cls]
