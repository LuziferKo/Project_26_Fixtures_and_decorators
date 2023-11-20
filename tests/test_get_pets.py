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


@pytest.mark.pets
@pytest.mark.parametrize('filter', [generate_string(255), generate_string(1001), russian_chars(),
                                    russian_chars().upper(), chinese_chars(), special_chars(), 123],
                         ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials'
                             , 'digit'])
def test_get_all_pets_with_negative_filter(filter):
    pytest.status, result = pf.get_list_of_pets(pytest.key, filter)

    # Проверяем статус ответа
    assert pytest.status == 400


@pytest.mark.parametrize('filter',
                       ['', 'my_pets'],
                       ids=['empty string', 'only my pets'])
def test_get_all_pets_with_valid_key(filter):
    """Проверяем, что на запрос всех питомцев возвращается не пустой список.
    Для этого сначала получаес api ключ и сохраняем его в переменную auth_key. Далее, используя этот ключ, запрашиваем
    список всех питомцев и проверяем, что он не пустой. Доступные занчения для параметра filter: 'my_pets или '' """

    pytest.status, result = pf.get_list_of_pets(pytest.key, filter)

    assert pytest.status == 200
    assert len(result['pets']) > 0
