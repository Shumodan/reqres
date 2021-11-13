from random import choice

import allure
import pytest

from libs.clients.errors.http_errors import HttpNotFound


class TestResources:
    @allure.title('Получение списка ресурсов без параметров')
    def test_get_resources(self, api):
        api.resources.get_all_resources()

    @allure.title('Постраничное получение списка всех ресурсов')
    def test_get_all_resource_pages(self, api):
        resources = api.resources.get_all_resources()
        with allure.step('Постраничное получение ресурсов'):
            for num in range(1, resources.total_pages + 1):
                api.resources.get_all_resources(page=num)

    @allure.title('Несуществующая страница не содержит данных')
    def test_get_non_existing_page(self, api):
        resources = api.resources.get_all_resources()
        result = api.resources.get_all_resources(page=resources.total_pages + 1)
        with allure.step('Проверка на пустоту данных'):
            assert result.data == []

    @allure.title('Ресурсы не пересекаются при постраничном выводе')
    def test_pages_contain_own_resources(self, api):
        page1 = {item.id for item in api.resources.get_all_resources(page=1).data}
        page2 = {item.id for item in api.resources.get_all_resources(page=2).data}
        with allure.step('Проверка данных на пересечение'):
            assert page1 & page2 == set()

    @allure.title('Можно получить существующий ресурс')
    def test_get_existing_resource(self, api):
        with allure.step('Выбрать любой существующий ресурс'):
            resource = choice(api.resources.get_all_resources().data)
        api.resources.get_resource(resource.id)

    @allure.title('Нельзя получить несуществующий ресурс')
    def test_get_non_existing_resource(self, api):
        with allure.step('Сгенерировать несуществующий id'):
            resources = api.resources.get_all_resources()
            resource_id = resources.total_pages * resources.total
        with pytest.raises(HttpNotFound):
            api.resources.get_resource(resource_id)
