import pytest
from settings import valid_email, valid_password
from datetime import datetime
from api import PetFriends

pf = PetFriends()


@pytest.fixture
def get_key():
    status, result = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in result
    return result


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print(f'\n Test duration: {end_time - start_time}')
