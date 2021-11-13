Требования
===
* минимальная версия языка: python >= 3.9
* пакет pipenv 
* allure для просмотра отчета https://github.com/allure-framework/allure2 

Установка и запуск
===
Вариант 1
---
1. Клонировать проект
2. Перейти в каталог проекта 
3. Выполнить `pipenv install`
4. Для запуска тестов выполнить `pipenv run tests`
5. Для просмотра отчета выполнить `allure serve _out/allure_report`

Вариант 2
---
1. Клонировать проект
2. Перейти в каталог проекта 
3. Выполнить `pipenv install`
4. Выполнить переход в виртуальное окружение `pipenv shell`
5. Запустить тесты `pytest tests`
6. Для просмотра отчета выполнить `allure serve _out/allure_report`