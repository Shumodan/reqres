import allure

from core.api.base_api import BaseApi
from core.models.resources import SingleResource, ListOfResources


class Resources(BaseApi):
    url = '/api/unknown'

    @allure.step('Получить ресурс')
    def get_resource(self, rid) -> SingleResource:
        return SingleResource.from_dict(
            self._client.get(f'{self.url}/{rid}')
        )

    @allure.step('Получить список ресурсов')
    def get_all_resources(self, **params) -> ListOfResources:
        return ListOfResources.from_dict(
            self._client.get(self.url, params=params)
        )
