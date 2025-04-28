from pydantic_settings import BaseSettings


class Configuration(BaseSettings):
    hello_template: str = "Ciao %s!"

    # Add any additional configuration needed for the ReAct agent
    enable_search: bool = True
    enable_calculator: bool = True
