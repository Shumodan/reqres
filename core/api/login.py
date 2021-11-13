import allure

from core.api.base_api import BaseApi
from core.models.auth import AuthenticationInfo


class Login(BaseApi):
    url = '/api/login'

    @allure.step('Аутентифицировать пользователя')
    def login(self, **kwargs) -> AuthenticationInfo:
        return AuthenticationInfo.from_dict(
            self._client.post(
                self.url,
                json=kwargs
            )
        )
