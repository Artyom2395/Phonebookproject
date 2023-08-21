# Phonebookproject
"""
Управление телефонным справочником.

Данный скрипт предоставляет управление телефонным справочником через командную строку.
С помощью этого скрипта можно выполнять операции добавления, редактирования, поиска и вывода контактов.

Для использования скрипта, выполните команду python manage.py console_command <команда> [доп.параметры].
Сам скрпит находится в phonebook\management\commands\console_command.py

Доступные команды:
- list: Вывести список всех контактов в телефонном справочнике.
- add: Добавить новый контакт в телефонный справочник.
- edit: Редактировать существующий контакт в телефонном справочнике.
- search: Выполнить поиск контактов на основе указанных критериев(в консоли будет задан вопрос о критерии поиска, и конкретном значении поиска).

Примеры использования:
- python manage.py console_command list
- python manage.py console_command add
- python manage.py console_command edit --id 1
- python manage.py console_command search

Телефонная книга сохраняется как в базе данных(стандартная SQLite), так и автоматически записывается в CSV-файл - 'contacts.csv'.
Редактирвание адаптировано как для базы данных, так и для'contacts.csv'.
Для добавления, редактирования и вывода контактов используется модель Contact с полями:
- first_name (Имя)
- last_name (Фамилия)
- middle_name (Отчество)
- organization (Организация)
- work_phone (Рабочий телефон)
- personal_phone (Личный телефон)
Для использования нужно выполнить миграции:
python manage.py makemigrations
python manage.py migrate

"""