import json
import os
from typing import Any, Dict


class Config:
    """
    A class to manage the configuration of the bot.
    """

    def __init__(self) -> None:
        self._load_config()

    def __str__(self) -> str:
        return str(self.config)

    def _load_config(self) -> Dict:
        if not os.path.exists("config.json"):
            raise FileNotFoundError("Configuration file not found.")
        with open("config.json", encoding="utf-8") as config_file:
            self.config = json.loads(config_file.read())
            return self.config
        
    def _update_config(self) -> None:
        with open("config.json", "w", encoding="utf-8") as config_file:
            json.dump(self.config, config_file, indent=4)

    def get_config(self) -> Dict:
        """
        Returns the configuration as a dictionary.

        Returns:
            Dict: The configuration as a dictionary.
        """
        return self._load_config()

    def set_config(self, key: str, value: Any) -> None:
        """
        Sets a configuration key to a value.

        Args:
            key (str): The key to set.
            value (Any): The value to set.
        """
        self.config[key] = value
        self._update_config()

class BotConfig:
    """
    A class to manage the bot information.
    """

    BOT_CONFIG_KEY = "BOT"
    BOT_CONFIG_NAME_KEY = "NAME"
    BOT_CONFIG_VERSION_KEY = "VERSION"

    def __init__(self) -> None:
        self.config = Config()
        self._load_bot_config()

    def _load_bot_config(self) -> Dict:
        self.bot_config = self.config.get_config()[self.BOT_CONFIG_KEY]
        return self.bot_config

    def _update_bot_config(self) -> None:
        self.config.set_config(self.BOT_CONFIG_KEY, self.bot_config)
        self._load_bot_config()
    
    def get_bot_version(self) -> str:
        """
        Returns the bot version.

        Returns:
            Version (str): The bot version.
        """
        return self._load_bot_config()[self.BOT_CONFIG_VERSION_KEY]
    
    def set_bot_name(self, name: str) -> None:
        """
        Set the bot name.

        Args:
            Name (str): The bot name.
        """
        self.bot_config[self.BOT_CONFIG_NAME_KEY] = name
        self._update_bot_config()


class TicketConfig:
    """
    A class to manage the ticket configuration of the bot.
    """

    TICKET_CONFIG_KEY = "TICKETS"
    TICKET_CONFIG_CATEGORY_KEY = "CATEGORY"

    def __init__(self) -> None:
        self.config = Config()
        self._load_ticket_config()

    def _load_ticket_config(self) -> Dict:
        self.ticket_config = self.config.get_config()[self.TICKET_CONFIG_KEY]
        return self.ticket_config

    def _update_ticket_config(self) -> None:
        self.config.set_config(self.TICKET_CONFIG_KEY, self.ticket_config)
        self._load_ticket_config()

    def get_ticket_category(self) -> int:
        """
        Returns ticket category ID.

        Returns:
            Category ID (int): The ticket category ID.
        """
        return self._load_ticket_config()[self.TICKET_CONFIG_CATEGORY_KEY]
    
    def set_ticket_category(self, category: int) -> None:
        """
        Set ticket category ID.

        Args:
            Category ID (int): The ticket category ID.
        """
        self.ticket_config[self.TICKET_CONFIG_CATEGORY_KEY] = category
        self._update_ticket_config()

class SchoolConfig:
    """
    A class to get schools role ID.
    """

    SCHOOLS_CONFIG_KEY = "SCHOOLS"

    def __init__(self) -> None:
        self.config = Config()
        self._load_schools_config()

    def _load_schools_config(self) -> Dict:
        self.schools_config = self.config.get_config()[self.SCHOOLS_CONFIG_KEY]
        return self.schools_config

    def _update_schools_config(self) -> None:
        self.config.set_config(self.SCHOOLS_CONFIG_KEY, self.schools_config)
        self._load_schools_config()

    def get_all_schools(self) -> dict[int]:
        """
        Returns the schools roles ID.

        Returns:
            Roles ID (dict[str:int]): The schools roles ID.
        """
        return self._load_schools_config()
    
    def get_school(self, school: str) -> int:
        """
        Returns the school role ID.

        Returns:
            Role ID (int): The school role ID.
        """
        if not school in self.get_all_schools():
            raise ValueError("School not found.")
        return self.get_all_schools()[school]
    
    def set_school(self, school: str, role_id: int) -> None:
        """
        Set the school role ID.

        Args:
            Role ID (int): The school role ID.
        """
        if not school in self.get_all_schools():
            raise ValueError("School not found.")
        
        self.get_all_schools()[school] = role_id
        self._update_schools_config()

class LogConfig:
    """
    A class to manage the logs system of the bot.
    """

    LOGS_CONFIG_KEY = "LOGS"
    LOGS_CONFIG_CHANNEL_KEY = "CHANNEL_ID"

    def __init__(self) -> None:
        self.config = Config()
        self._load_logs_config()

    def _load_logs_config(self) -> Dict:
        self.logs_config = self.config.get_config()[self.LOGS_CONFIG_KEY]
        return self.logs_config

    def _update_logs_config(self) -> None:
        self.config.set_config(self.LOGS_CONFIG_KEY, self.logs_config)
        self._load_logs_config()

    def get_logs_active(self) -> list[str]:
        """
        Returns active scopes.

        Returns:
            Scopes (list): The active scopes.
        """
        active_scopes = [scope for scope, status in self._load_logs_config().items() if status and scope != self.LOGS_CONFIG_CHANNEL_KEY]
        return active_scopes
    
    def get_logs_channel(self) -> int:
        """
        Returns the channel ID where logs info will be displayed.

        Returns:
            Channel ID (int): The channel ID where logs info will be displayed.
        """
        return self._load_logs_config()[self.LOGS_CONFIG_CHANNEL_KEY]
    
    def set_logs_channel(self, channel_id: int) -> None:
        """
        Set the channel where logs info will be displayed.

        Args:
            Channel ID (int): The channel ID where logs info will be displayed.
        """
        self.logs_config[self.LOGS_CONFIG_CHANNEL_KEY] = channel_id
        self._update_logs_config()
    
