from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json, Undefined

from core.models.system import SupportInfo


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class Resource:
    id: int
    name: str
    year: int
    color: str
    pantone_value: str


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class SingleResource:
    data: Resource
    support: SupportInfo


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class ListOfResources:
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[Resource]
    support: SupportInfo
