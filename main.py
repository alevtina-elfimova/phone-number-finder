from phone_number_finder import (
    find_phone_numbers,
    find_phone_numbers_in_file,
    find_phone_numbers_on_webpage,
    is_valid_phone_number,
)

def main():
    """Запуск главного меню программы"""
    while True:
        print('\n Поиск и проверка телефонных номеров')
        print('1. Проверить один телефонный номер')
        print('2. Найти номер в тексте')
        print('3. Найти номера в файле')
        print('4. Найти номера на веб-странице')
        print('5. Выход')

        choice = input('Выберите действие:')

        if choice == '5':
            print('Работа программы завершена')
            break

        elif choice == '1':
            phone = input('Введите телефонный номер: ')

            if is_valid_phone_number(phone):
                print('Номер соответствует заданному формату')
            else:
                print('Номер не соответствует заданному формату')

        elif choice == '2':
            print('Введите текст для поиска номеров.')
            print('Для завершения ввода нажмите Enter на пустой строке.')

            lines = []

            while True:
                line = input()

                if not line:
                    break

                lines.append(line)

            text = '\n'.join(lines)
            phone_numbers = find_phone_numbers(text)

            if phone_numbers:
                print('Найденные телефонные номера:')
                for phone in phone_numbers:
                    print(phone)
            else:
                print('Телефонные номера не найдены')

        elif choice == '3':
            file_path = input('Введите путь к текстовому файлу: ')

            try:
                phone_numbers = find_phone_numbers_in_file(file_path)

                if phone_numbers:
                    print('Найденные телефонные номера:')
                    for phone in phone_numbers:
                        print(phone)
                else:
                    print('Телефонные номера не найдены')

            except ValueError as error:
                print(error)

        elif choice == '4':
            url = input('Введите адрес веб-страницы: ')

            try:
                phone_numbers = find_phone_numbers_on_webpage(url)

                if phone_numbers:
                    print('Найденные телефонные номера:')
                    for phone in phone_numbers:
                        print(phone)
                else:
                    print('Телефонные номера не найдены')

            except ValueError as error:
                print(error)

        else:
            print('Неверный выбор, попробуйте ещё раз')

if __name__ == '__main__':
    main()
