import os
import json
from typing import Any, Dict

class ConfigUtils:

    @staticmethod
    def get_config():
        if not os.path.exists("config.json"):
            raise FileNotFoundError("Configuration file not found.")
        with open("config.json", encoding="utf-8") as config_file:
            return json.loads(config_file.read())

    @staticmethod
    def get_config_value(value_name: str) -> str | int | Dict:
        config = ConfigUtils.get_config()
        return config[value_name] 

    @staticmethod
    def set_config_value(value_name: str, value_content: Any) -> None:
        config = ConfigUtils.get_config()

        config[value_name] = value_content

        with open('config.json', encoding='utf-8') as config_file:
            config_file.write(json.dumps(config))

