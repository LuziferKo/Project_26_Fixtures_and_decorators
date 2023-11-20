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
@pytest.mark.parametrize('age', [1], ids=['min'])
def test_successful_update_self_pet_info(name, animal_type, age):
    """Проверяем, что можно обновить данные питомца из списка своих питомцев"""

    # Получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')

    # Если список не пустой, пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        pytest.status, result = pf.update_info_about_pet(pytest.key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем, что статус ответа = 200 и имя питомца соответствует заданному
        assert pytest.status == 200
        assert result['name'] == name
    else:
        # Если список питомцев пустой, то вызываем исключение с текстом об отсутствии своих питомцев
        raise Exception('There is no My pets')


@pytest.mark.pets
@pytest.mark.parametrize('pet_photo', ['images/George.jpeg', 'images/cat.png'], ids=['jpeg', 'png'])
def test_successful_add_photo(pet_photo):
    """Проверяем возможность добавить фото питомца"""

    # Получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')

    # Получаем полный путь изображения питомца и сохраняем его в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Если список не пустой, пробуем добавить фото для первого питомца
    if len(my_pets['pets']) > 0:
        pytest.status, result = pf.add_photo(pytest.key, my_pets['pets'][0]['id'], pet_photo)

        assert pytest.status == 200
        assert result['pet_photo'] == pet_photo
    else:
        raise Exception('There is no My pets')


@pytest.mark.pets
@pytest.mark.parametrize('pet_photo', ['images/cat.gif', 'images/tiger.webp'], ids=['gif', 'webp'])
def test_add_photo_wrong_extension(pet_photo):
    """Проверяем, что при загрузке фото с неверным расширением файла система выдаст ошибку"""

    _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    if len(my_pets['pets']) > 0:
        pytest.status, result = pf.add_photo(pytest.key, my_pets['pets'][0]['id'], pet_photo)

        assert pytest.status == 500
    else:
        raise Exception('There is no My pets')


@pytest.mark.pets
def test_update_only_name(name='Барсик', animal_type='', age=''):
    """Проверяем, что можно изменить только имя питомца"""

    _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')

    if len(my_pets['pets']) > 0:
        pytest.status, result = pf.update_info_about_pet(pytest.key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert pytest.status == 200
        assert result['name'] == name
    else:
        raise Exception('There is no My pets')


@pytest.mark.pets
def test_successful_delete_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')

    # Проверяем, если список своих питомцев пустой, то добавляем нового и опрять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_info_about_new_pet(pytest.key, 'Барсик', 'кот', '8', 'images/Barsik.jpeg')
        _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(pytest.key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')

    # Проверяем, что статус ответа 200 и в списке питомцев не id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()