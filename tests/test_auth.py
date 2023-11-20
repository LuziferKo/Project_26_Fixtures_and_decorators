import os.path
from api import PetFriends
import pytest
from settings import valid_email, valid_password, invalid_password, invalid_email


pf = PetFriends()


def generate_string(n):
    return 'x' * n

def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


@pytest.mark.auth
@pytest.mark.parametrize('email', [valid_email], ids=['valid_email'])
@pytest.mark.parametrize('password', [valid_password], ids=['valid_password'])
def test_get_api_key_for_valid_user(email, password):
    """Проверяем, что запрос API ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    pytest.status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с ожидаемым результатом
    assert pytest.status == 200
    assert 'key' in result


@pytest.mark.auth
@pytest.mark.parametrize('email', ['', valid_email, invalid_email, 'test567@test', '123456',
                                   generate_string(256)],
                         ids=['empty', 'valid_email', 'invalid_email', 'wrong_email_format', 'digits', 'max'])
@pytest.mark.parametrize('password', ['', invalid_password, russian_chars(), russian_chars().upper, chinese_chars(),
                                      special_chars()],
                         ids=['empty', 'invalid_pass', 'russian', 'RUSSAIN', 'chinese', 'special'])
def test_get_auth_key_negative(email, password):
    """Проверяем, что при вводе незарегистрированного email и пароля система выдаст ошибку"""

    pytest.status, result = pf.get_api_key(email, password)
    assert pytest.status == 403
