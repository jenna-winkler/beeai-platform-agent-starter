from pydantic_settings import BaseSettings


class Configuration(BaseSettings):
    debug_mode: bool = False