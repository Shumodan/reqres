import allure

from core.api.base_api import BaseApi
from core.models.auth import RegistrationInfo


class Register(BaseApi):
    url = '/api/register'

    @allure.step('Зарегистрировать пользователя')
    def register_user(self, **kwargs) -> RegistrationInfo:
        return RegistrationInfo.from_dict(
            self._client.post(
                self.url,
                json=kwargs
            )
        )
