import re
import requests


#Регулярное выражение для поиска российских номеров телефона
PHONE_PATTERN = re.compile(
    r'(?<!\w)(?:\+7|8)[ -]?(?:\(\d{3}\)|\d{3})'
    r'[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}(?!\w)'
)

def find_phone_numbers(text):
    """Находит все телефонные номера в переданном тексте"""
    return PHONE_PATTERN.findall(text)

def is_valid_phone_number(phone):
    """Проверяет, соответствует ли введённый номер заданному формату"""
    return PHONE_PATTERN.fullmatch(phone) is not None

def find_phone_numbers_in_file(file_path):
    """Находит номера телефонов в текстовом файле"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        return find_phone_numbers(text)

    except (OSError, UnicodeDecodeError) as error:
        raise ValueError(f'Не удалось прочитать файл: {error}') from error

def find_phone_numbers_on_webpage(url):
    """Находит номера на веб-странице"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        return find_phone_numbers(response.text)

    except requests.RequestException as error:
        raise ValueError(
            f'Не удалось получить содержимое веб-страницы: {error}'
        ) from error

