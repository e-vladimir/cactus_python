# ОБРАБОТЧИКИ ДАТЫ/ВРЕМЕНИ
# 2023-07-12

import time


# UNIX-ВРЕМЯ
def CurrentUTime() -> int:
	""" Получение текущего времени в UNIX-формате """
	return int(time.time())
