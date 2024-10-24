# Тестирование
Зависимости указаны в requirements.tests.txt
Инсталляция:
> `pip -r requirements.tests.txt`

Конфигурация тестов указана в файле `tests/pytest.ini`
Запуск тестов осуществляется утилитой `pytest`
Примеры запусков:
> `PYTHONPATH="G0:G1:G2:G3" pytest tests -m 'sqlite and not perfomance'`
 
> `pytest tests -m 'sql'`

> `pytest tests`

Файлы с тестами должны начинаться на `check_*` (настраивается в конфигурации)
**pytest** запускает методы как тестировочные начинающиеся с `test_*`
