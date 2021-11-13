from dataclasses import dataclass

from dataclasses_json import dataclass_json, Undefined


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class SupportInfo:
    url: str
    text: str
