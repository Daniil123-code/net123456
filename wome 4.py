documents = [
    {'type': 'passport', 'number': '2207 876234', 'name': 'Василий Гупкин'},
    {'type': 'invoice', 'number': '11-2', 'name': 'Геннадий Покемонов'},
    {'type': 'insurance', 'number': '10006', 'name': 'Аристарх Павлов'}
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}


def get_owner_by_number():
    doc_number = input("Введите номер документа: ")
    for doc in documents:
        if doc['number'] == doc_number:
            print(f"Результат:\nВладелец документа: {doc['name']}")
            return
    print("Документ не найден")


def get_shelf_by_number():
    doc_number = input("Введите номер документа: ")
    for shelf, docs in directories.items():
        if doc_number in docs:
            print(f"Результат:\nДокумент хранится на полке: {shelf}")
            return
    print("Документ на полках не найден")


while True:
    command = input("Введите команду: ").lower()

    if command == 'p':
        get_owner_by_number()
    elif command == 's':
        get_shelf_by_number()
    elif command == 'q':
        print("Программа завершена.")
        break