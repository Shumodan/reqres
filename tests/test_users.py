from contextlib import nullcontext
from random import choice
from uuid import uuid4

import allure
import pytest

from libs.clients.errors.http_errors import HttpNotFound, HttpBaseError, HttpBadRequest

USER_DATA = (
    dict(name=f'Test{uuid4().hex}'),
    dict(name=f'Тест{uuid4().hex}', job='Student'),
    dict(name=f'Test{uuid4().hex}' * 100, job='Student'),
    dict(name=f'{uuid4().hex}', phone='+70000000001')
)

USER_AUTH_DATA = [
    (dict(email='eve.holt@reqres.in', password='qqq'), nullcontext()),
    (dict(email=f'm{uuid4().hex}@mail.in', password='pass'), pytest.raises(HttpBadRequest)),
    (dict(password='pass'), pytest.raises(HttpBadRequest)),
    (dict(email=f'm{uuid4().hex}@mail.in'), pytest.raises(HttpBadRequest))
]


class TestUsersView:
    @allure.title('Получение списка пользователей без параметров')
    def test_get_users(self, api):
        api.users.get_users()

    @allure.title('Постраничное получение списка всех пользователей')
    def test_get_all_users_by_pages(self, api):
        users = api.users.get_users()
        with allure.step('Постраничное получение пользователей'):
            for num in range(1, users['total_pages'] + 1):
                api.users.get_users(page=num)

    @allure.title('Несуществующая страница не содержит данных')
    def test_get_non_existing_page(self, api):
        users = api.users.get_users()
        result = api.users.get_users(page=users['total_pages'] + 1)
        with allure.step('Проверка на пустоту данных'):
            assert result['data'] == []

    @allure.title('Пользователи не пересекаются при постраничном выводе')
    def test_pages_contain_own_users(self, api):
        page1 = {item['id'] for item in api.users.get_users(page=1)['data']}
        page2 = {item['id'] for item in api.users.get_users(page=2)['data']}
        with allure.step('Проверка данных на пересечение'):
            assert page1 & page2 == set()

    @allure.title('Можно получить существующего пользователя')
    def test_get_existing_user(self, api):
        with allure.step('Выбрать любого существующего пользователя'):
            user = choice(api.users.get_users()['data'])
        api.users.get_user(user['id'])

    @allure.title('Нельзя получить несуществующего пользователя')
    def test_get_non_existing_user(self, api):
        with allure.step('Сгенерировать несуществующий id'):
            users = api.users.get_users()
            user_id = users['total_pages'] * users['total']
        with pytest.raises(HttpNotFound):
            api.users.get_user(user_id)


class TestUsersModification:

    @allure.title('Создание пользователя с проверкой результата')
    def test_create_user(self, api):
        result = api.users.create_user(name=f'Test{uuid4().hex}', job='Student')
        try:
            api.users.get_user(result['id'])
        except HttpBaseError:
            assert False, 'Пользователь не был сохранен'

    @allure.title('Создание пользователя')
    @pytest.mark.parametrize('user_data', USER_DATA)
    def test_create_user_with_params(self, api, user_data):
        result = api.users.create_user(**user_data)
        with allure.step('Сравнение данных ответа с начальными параметрами'):
            assert result == result | user_data

    @allure.title('Редактирование с проверкой результата')
    def test_edit_user(self, api):
        new_data = dict(first_name=f'Name{uuid4().hex}')
        with allure.step('Получение пользователя для редактирования'):
            user_id = api.users.get_users()['data'][0]['id']
        api.users.update_user(user_id, **new_data)
        result = api.users.get_user(user_id)['data']
        with allure.step('Проверка отредактированного поля'):
            assert result == result | new_data, 'Данные пользователя не были отредактированы'

    @allure.title('Редактирование пользователя, проверка ответа')
    @pytest.mark.parametrize('user_data', USER_DATA)
    def test_edit_user_with_params(self, api, user_data):
        result = api.users.update_user(1, **user_data)
        with allure.step('Сравнение данных ответа с начальными параметрами'):
            assert result == result | user_data

    @allure.title('Удаление пользователя, проверка ответа')
    def test_delete_user(self, api):
        api.users.delete_user(300)

    @allure.title('Удаление пользователя, проверкой результата')
    def test_delete_user(self, api):
        with allure.step('Получение пользователя для удаления'):
            user_id = api.users.get_users()['data'][0]['id']
        api.users.delete_user(user_id)
        with pytest.raises(HttpNotFound):
            api.users.get_user(user_id)


class TestUsersAuth:

    @allure.title('Процедура регистрации пользователя')
    @pytest.mark.parametrize('user_auth_data, expected_result', USER_AUTH_DATA)
    def test_register_user(self, api, user_auth_data, expected_result):
        with expected_result:
            api.register.register_user(**user_auth_data)

    @allure.title('Аутентификация пользователя')
    @pytest.mark.parametrize('user_auth_data, expected_result', USER_AUTH_DATA)
    def test_auth_user(self, api, user_auth_data, expected_result):
        with expected_result:
            api.auth.login(**user_auth_data)
