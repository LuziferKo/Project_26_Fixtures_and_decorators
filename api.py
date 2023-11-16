import requests
import json
import pytest
import logging
from requests_toolbelt.multipart.encoder import MultipartEncoder


logger = logging.getLogger('requests')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('log.txt')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)

def log_requests(func):
    def wrapper(*args, **kwargs):
        # Логируем запрос
        logger.info('Request:')
        # logger.info('URL: {}'.format(args[0]))
        logger.info('Method: {}'.format(func.__name__))
        logger.info('Arguments: {}'.format(args[1:]))
        logger.info('Keyword Arguments: {}'.format(kwargs))

        # Вызываем функцию и получаем результат
        result = func(*args, **kwargs)

        # Логируем ответ
        logger.info('Response:')
        logger.info('Status Code: {}'.format(result[0]))
        logger.info('Response Body: {}'.format(result[1]))

        # Возвращаем результат
        return result
    return wrapper


class PetFriends:
    """API библиотека к веб-приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    @log_requests
    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключом пользователя, найденным по указанным email и паролю"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + "api/key", headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @log_requests
    def create_pet_simple(self, auth_key, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет на сервер данные о добавлении питомца (без фото) и возвращает статус
        запроса на сервер и результат в формате json о добавленном питомце"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @log_requests
    @pytest.mark.pets
    def get_list_of_pets(self, auth_key: json, filter) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком найденных питомцев, совпадающих с фильтром. На данный момент может иметь либо пустое
        значение (получить список всех питомцев), либо 'my_pets' (получить список собственных питомцев)"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @log_requests
    @pytest.mark.pets
    def add_info_about_new_pet(self, auth_key: json, name: str,
                               animal_type: str, age: int, pet_photo: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце и возвращает статус запроса на сервер
        и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    @log_requests
    @pytest.mark.pets
    def add_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет на сервер данные о добавлении фото питомца по id и возвращает статус запроса
        на сервер и результат в формате JSON с данными питомца"""
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
            result['pet_photo'] = pet_photo
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    @log_requests
    @pytest.mark.pets
    def update_info_about_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет на сервер запрос об обновлении данных питомца с указанным id и возвращает
        статус запроса и результат в формате json с обновлёнными данными питомца"""

        headers = {'auth_key': auth_key['key']}

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    @log_requests
    @pytest.mark.pets
    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает статус
        запроса и результат в формате JSON с текстовым уведомлением об успешном удалении.
        На текущий момент есть баг: в result приходит пустая строка, но при этом status = 200"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result
