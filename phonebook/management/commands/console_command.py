import csv
from django.core.management.base import BaseCommand
from phonebook.models import Contact

class Command(BaseCommand):
    help = 'Управление телефонным справочником'

    def add_arguments(self, parser):
        parser.add_argument('command', type=str, help="Доступные команды: list, add, edit, search")
        parser.add_argument('--id', type=int, help="ID контакта для редактирования")

    def handle(self, *args, **options):
        """
        Обработка выполнения основной команды на основе указанной команды в аргументах.
        """
        command = options['command']
        if command == 'list':
            self.list_contacts()
        elif command == 'add':
            self.add_contact()
        elif command == 'edit':
            contact_id = options['id']
            if contact_id:
                self.edit_contact(contact_id)
            else:
                print("Пожалуйста, укажите ID контакта для редактирования")
        elif command == 'search':
            self.search_contacts()
        else:
            print("Недопустимая команда")

    def list_contacts(self) -> None:
        """
        Вывод всех контактов в телефонном справочнике.
        """
        contacts = Contact.objects.all()
        for contact in contacts:
            print(f"ID: {contact.id}")
            print(f"ФИО: {contact.last_name} {contact.first_name} {contact.middle_name}")
            print(f"Организация: {contact.organization}")
            print(f"Рабочий телефон: {contact.work_phone}")
            print(f"Личный телефон: {contact.personal_phone}")
            print("-" * 30)

    def add_contact(self) -> None:
        """
        Добавление нового контакта в телефонный справочник.
        """
        first_name = input("Введите имя: ")
        last_name = input("Введите фамилию: ")
        middle_name = input("Введите отчество: ")
        organization = input("Введите организацию: ")
        work_phone = input("Введите рабочий телефон: ")
        personal_phone = input("Введите личный телефон: ")


        contact = Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            organization=organization,
            work_phone=work_phone,
            personal_phone=personal_phone
        )
        print("Контакт успешно добавлен")

        #Записываем контакт в файл
        self.write_contact_to_csv(contact)

    def write_contact_to_csv(self, contact: Contact)-> None:
        """
        Запись нового контакта в CSV-файл.
        """
        filename = 'contacts.csv'

        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ID', 'Имя', 'Фамилия', 'Отчество', 'Организация', 'Рабочий телефон', 'Личный телефон']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Проверяем, нужно ли записать заголовки
            if csvfile.tell() == 0:
                writer.writeheader()

            # Записываем данные нового контакта
            writer.writerow({
                'ID': contact.id,
                'Имя': contact.first_name,
                'Фамилия': contact.last_name,
                'Отчество': contact.middle_name,
                'Организация': contact.organization,
                'Рабочий телефон': contact.work_phone,
                'Личный телефон': contact.personal_phone
            })
            print("Контакт добавлен в CSV")
    
    def edit_contact(self, contact_id: int) -> None:
        """
        Редактирование существующего контакта в телефонном справочнике.
        """
        try:
            contact = Contact.objects.get(id=contact_id)
            first_name = input(f"Введите новое имя ({contact.first_name}): ")
            last_name = input(f"Введите новую фамилию ({contact.last_name}): ")
            middle_name = input(f"Введите новое отчество ({contact.middle_name}): ")
            organization = input(f"Введите новую организацию ({contact.organization}): ")
            work_phone = input(f"Введите новый рабочий телефон ({contact.work_phone}): ")
            personal_phone = input(f"Введите новый личный телефон ({contact.personal_phone}): ")

            contact.first_name = first_name if first_name else contact.first_name
            contact.last_name = last_name if last_name else contact.last_name
            contact.middle_name = middle_name if middle_name else contact.middle_name
            contact.organization = organization if organization else contact.organization
            contact.work_phone = work_phone if work_phone else contact.work_phone
            contact.personal_phone = personal_phone if personal_phone else contact.personal_phone

            contact.save()

            #Обновляем информацию в файле
            self.update_csv_file(contact)

            print("Контакт успешно обновлен")
        except Contact.DoesNotExist:
            print(f"Контакт с ID {contact_id} не найден")
    
    def update_csv_file(self, contact: Contact) -> None:
        """
        Обновление информации о контакте в CSV-файле.
        """

        filename = 'contacts.csv'
        updated_contacts = []

        # Читаем данные из CSV файла
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['ID']) == contact.id:
                    row['Имя'] = contact.first_name
                    row['Фамилия'] = contact.last_name
                    row['Отчество'] = contact.middle_name
                    row['Организация'] = contact.organization
                    row['Рабочий телефон'] = contact.work_phone
                    row['Личный телефон'] = contact.personal_phone
                updated_contacts.append(row)

        # Записываем обновленные данные обратно в CSV файл
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ID', 'Имя', 'Фамилия', 'Отчество', 'Организация', 'Рабочий телефон', 'Личный телефон']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in updated_contacts:
                writer.writerow(row)
    
    def search_contacts(self) -> None:
        """
        Поиск контактов в телефонном справочнике на основе указанных критериев поиска.
        """
        
        field_mapping = {
            'имя': 'first_name',
            'фамилия': 'last_name',
            'отчество': 'middle_name',
            'организация': 'organization',
            'рабочий телефон': 'work_phone',
            'личный телефон': 'personal_phone',
            'id': 'id'
        }

        print("Доступные критерии поиска:")
        for russian_name, db_field in field_mapping.items():
            print(f"{russian_name.capitalize()} ({db_field.capitalize()})")

        while True:
            search_criterion = input("Введите критерий поиска (на русском или английском): ").lower()
            
            # Проверка, что пользовательский ввод соответствует критериям
            if search_criterion in field_mapping:
                break
            else:
                print("Некорректный критерий поиска. Пожалуйста, повторите ввод.")

        search_value = input("Введите значение для поиска: ")

        if field_mapping[search_criterion] == 'id':
            search_kwargs = {
                field_mapping[search_criterion]: search_value
            }
        else:
            search_kwargs = {
                f"{field_mapping[search_criterion]}__icontains": search_value
            }

        contacts = Contact.objects.filter(**search_kwargs)

        print(f"Найдено {contacts.count()} контактов")
        for contact in contacts:
            print(f"ID: {contact.id}")
            print(f"ФИО: {contact.last_name} {contact.first_name} {contact.middle_name}")
            print(f"Организация: {contact.organization}")
            print(f"Рабочий телефон: {contact.work_phone}")
            print(f"Личный телефон: {contact.personal_phone}")
            print("-" * 30)