import os.path
from api import PetFriends
import pytest


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
@pytest.mark.parametrize('name', [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
                                  chinese_chars(), special_chars(), '123'],
                         ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials',
                              'digit'])
@pytest.mark.parametrize('animal_type', [generate_string(255), generate_string(1001), russian_chars(),
                                         russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                         ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials',
                              'digit'])
@pytest.mark.parametrize('age', ['1'], ids=['min'])
@pytest.mark.parametrize('pet_photo', ['images/George.jpeg', 'images/cat.png'], ids=['jpeg', 'png'])
def test_add_new_pet_with_valid_data(name, animal_type, age, pet_photo):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем его в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем питомца
    pytest.status, result = pf.add_info_about_new_pet(pytest.key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert pytest.status == 200
    assert result['name'] == name


@pytest.mark.pets
@pytest.mark.parametrize('name', [''], ids=['empty'])
@pytest.mark.parametrize('animal_type', [''], ids=['empty'])
@pytest.mark.parametrize('age', ['', '-1', '0', '100', '1.5', '2147483647', '2147483648',
                                 special_chars(), russian_chars(), russian_chars().upper, chinese_chars()],
                         ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1',
                         'specials', 'russian', 'RUSSIAN', 'chinese'])
@pytest.mark.parametrize('pet_photo', ['images/cat.gif', 'images/tiger.webp'], ids=['gif', 'webp'])
def test_add_new_pet_negative(name, animal_type, age, pet_photo):
    """Проверяем, что при попытке создания питомца без обязательного поля Имя система выдаст ошибку"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    pytest.status, result = pf.add_info_about_new_pet(pytest.key, name, animal_type, age, pet_photo)

    assert pytest.status == 400


@pytest.mark.parametrize('name', [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(),
                                  chinese_chars(), special_chars(), '123'],
                         ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials',
                              'digit'])
@pytest.mark.parametrize('animal_type', [generate_string(255), generate_string(1001), russian_chars(),
                                         russian_chars().upper(), chinese_chars(), special_chars(), '123'],
                         ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials',
                              'digit'])
@pytest.mark.parametrize('age', [1], ids=['min'])
def test_add_new_pet_simple(name, animal_type, age):
    """ Проверяем, что можно добавить питомца с различным данными"""

    # Добавляем питомца
    pytest.status, result = pf.add_new_pet_simple(pytest.key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert pytest.status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type


@pytest.mark.parametrize('name', [''], ids=['empty'])
@pytest.mark.parametrize('animal_type', [''], ids=['empty'])
@pytest.mark.parametrize('age', ['', '-1', '0', '100', '1.5', '2147483647', '2147483648',
                                 special_chars(), russian_chars(), russian_chars().upper, chinese_chars()],
                         ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1',
                              'specials', 'russian', 'RUSSIAN', 'chinese'])
def test_add_new_pet_simple_negative(name, animal_type, age):

    pytest.status, result = pf.add_new_pet_simple(pytest.key, name, animal_type, age)

    assert pytest.status == 400
