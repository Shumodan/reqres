from dataclasses import dataclass

from dataclasses_json import dataclass_json, Undefined


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class RegistrationInfo:
    id: int
    token: str


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class AuthenticationInfo:
    token: str
