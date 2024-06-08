# ОБРАБОТЧИКИ ДАТЫ/ВРЕМЕНИ
# 08 июн 2024

import time


# UNIX-ВРЕМЯ
def CurrentUTime() -> int:
	""" Получение текущего времени в UNIX-формате """
	return int(time.time())
