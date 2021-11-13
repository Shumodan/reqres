from dataclasses import dataclass


@dataclass(frozen=True)
class SystemConfig:
    host_url: str = 'https://reqres.in'


config = SystemConfig()
