import allure

from core.api.base_api import BaseApi


class Users(BaseApi):
    url = '/api/users'

    @allure.step('Получить список пользователей')
    def get_users(self, **params):
        return self._client.get(self.url, params=params)

    @allure.step('Получить пользователя')
    def get_user(self, user_id):
        return self._client.get(f'{self.url}/{user_id}')

    @allure.step('Создать пользователя')
    def create_user(self, name, **kwargs):
        return self._client.post(
            self.url, json=dict(name=name) | kwargs
        )

    @allure.step('Редактировать пользователя')
    def update_user(self, user_id, **kwargs):
        return self._client.put(
            f'{self.url}/{user_id}',
            json=kwargs
        )

    @allure.step('Редактировать поля пользователя')
    def update_user_partially(self, user_id, **kwargs):
        return self._client.put(
            f'{self.url}/{user_id}',
            json=kwargs
        )

    @allure.step('Удалить пользователя')
    def delete_user(self, user_id):
        return self._client.delete(f'{self.url}/{user_id}')
