import requests
import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from phone_number_finder import (
    find_phone_numbers_in_file,
    find_phone_numbers_on_webpage,
    find_phone_numbers,
    is_valid_phone_number,
)

class TestPhoneNumberValidation(unittest.TestCase):
    """Тесты для проверки корректности номеров"""

    def test_valid_phone_numbers(self):
        """Проверка по заданному формату"""
        valid_numbers = [
            '+79991234567',
            '+7 999 123 45 67',
            '+7 (999) 123-45-67',
            '89991234567',
            '8 999 123 45 67',
        ]
        for phone in valid_numbers:
            with self.subTest(phone=phone):
                self.assertTrue(is_valid_phone_number(phone))

    def test_invalid_phone_numbers(self):
        """Проверка номеров, которые не соответствуют заданному формату"""
        invalid_numbers = [
            '+7 (99) 123-45-67',
            '+7 999 123 45',
            '+7 ABC 123-45-67',
            '123456',
            '',
        ]

        for phone in invalid_numbers:
            with self.subTest(phone=phone):
                self.assertFalse(is_valid_phone_number(phone))

class TestPhoneNumberSearch(unittest.TestCase):
    """Тесты для поиска номеров в тексте"""

    def test_find_multiple_phone_numbers(self):
        """Проверка нескольких номеров"""
        text = (
            'Позвоните: +7 999 123-45-67 '
            'Дополнительный номер: 8 917 345-67-89'
        )
        expected = [
            '+7 999 123-45-67',
            '8 917 345-67-89',
        ]
        self.assertEqual(find_phone_numbers(text), expected)

    def test_find_no_phone_numbers(self):
        """Проверка текста, где нет номера"""
        text = 'В этом тексте нет телефонных номеров'
        self.assertEqual(find_phone_numbers(text), [])

    def test_find_phone_number_in_multiline_text(self):
        """Проверка поиска номеров в многострочном тексте"""
        text = (
            'Первый номер: +7 999 123-45-67.\n'
            'Второй номер: 8 912 345-67-89.'
        )
        expected = [
            '+7 999 123-45-67',
            '8 912 345-67-89',
        ]
        self.assertEqual(find_phone_numbers(text), expected)

class TestPhoneNumberFileSearch(unittest.TestCase):
    """Тесты для поиска номеров в файле"""

    def test_find_phone_numbers_in_file(self):
        """Проверка поиска номеров в существующем файле"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / 'phones.txt'
            file_path.write_text(
                'Первый номер: +7 999 123-45-67.\n'
                'Второй номер: 8 912 345-67-89.',
                encoding='utf-8'
            )
            expected = [
                '+7 999 123-45-67',
                '8 912 345-67-89',
            ]

            result = find_phone_numbers_in_file(file_path)
            self.assertEqual(result, expected)

    def test_file_without_phone_numbers(self):
        """Проверка файла без номеров"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / 'empty_phones.txt'

            file_path.write_text(
                'В этом файле нет номеров.',
                encoding='utf-8'
            )

            self.assertEqual(
                find_phone_numbers_in_file(file_path),
                []
            )

    def test_file_not_found(self):
        """Обработка отсутствующего файла"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / 'missing.txt'

            with self.assertRaises(ValueError):
                find_phone_numbers_in_file(file_path)

    def test_file_with_invalid_encoding(self):
        """Обработка файла с неподходящей кодировкой"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / 'invalid.txt'
            file_path.write_bytes(b'\xff\xfe')

            with self.assertRaises(ValueError):
                find_phone_numbers_in_file(file_path)


class TestPhonePageSearch(unittest.TestCase):
    """Тесты для поиска номеров с веб-страниц"""

    @patch('phone_number_finder.requests.get')
    def test_find_phone_numbers_on_webpage(self, mock_get):
        """Проверка поиска номера на веб-странице"""
        mock_response = Mock()
        mock_response.text = (
            'Наш номер: +7 999 123-45-67. '
            'Дополнительный номер: 8 912 345-67-89.'
        )
        mock_get.return_value = mock_response

        expected = [
            '+7 999 123-45-67',
            '8 912 345-67-89',
        ]

        result = find_phone_numbers_on_webpage(
            'https://example.com'
        )

        self.assertEqual(result, expected)
        mock_get.assert_called_once_with(
            'https://example.com',
            timeout=10
        )

    @patch('phone_number_finder.requests.get')
    def test_webpage_without_phone_numbers(self, mock_get):
        """Проверка веб-страницы без номеров"""
        mock_response = Mock()
        mock_response.text = 'На этой странице нет номеров.'
        mock_get.return_value = mock_response

        result = find_phone_numbers_on_webpage(
            'https://example.com'
        )

        self.assertEqual(result, [])

    @patch('phone_number_finder.requests.get')
    def test_webpage_request_error(self, mock_get):
        """Обработка ошибки запроса к сайту"""
        mock_get.side_effect = requests.ConnectionError(
            'Ошибка подключения'
        )

        with self.assertRaises(ValueError):
            find_phone_numbers_on_webpage(
                'https://example.com'
            )

    @patch('phone_number_finder.requests.get')
    def test_webpage_http_error(self, mock_get):
        """Обработка HTTP-ошибки при загрузке веб-страницы"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError(
            'Ошибка HTTP'
        )
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            find_phone_numbers_on_webpage('https://example.com')


if __name__ == '__main__':
    unittest.main()
