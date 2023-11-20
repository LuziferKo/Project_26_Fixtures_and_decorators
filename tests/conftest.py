import pytest
from settings import valid_email, valid_password
from datetime import datetime
from api import PetFriends

pf = PetFriends()


# @pytest.fixture
# def get_key():
#     status, result = pf.get_api_key(valid_email, valid_password)
#     assert status == 200
#     assert 'key' in result
#     return result


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print(f'\n Test duration: {end_time - start_time}')


@pytest.fixture(autouse=True)
def get_api_key():
    """Проверяем, что запрос api-ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    pytest.status, pytest.key = pf.get_api_key(valid_email, valid_password)

    # Сверяем полученные данные с нашими ожиданиями
    assert pytest.status == 200
    assert 'key' in pytest.key

    yield

    # Проверяем, что статус ответа = 200
    assert pytest.status == 200
