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


class TicketConfig:
    """
    A class to manage the ticket configuration of the bot.
    """

    TICKET_CONFIG_KEY = "TICKETS"
    TICKET_CONFIG_STATUS_KEY = "IS_ACTIVE"

    def __init__(self) -> None:
        self.config = Config()
        self._load_ticket_config()

    def _load_ticket_config(self) -> Dict:
        self.ticket_config = self.config.get_config()[self.TICKET_CONFIG_KEY]
        return self.ticket_config

    def _update_ticket_config(self) -> None:
        self.config.set_config(self.TICKET_CONFIG_KEY, self.ticket_config)
        self._load_ticket_config()

    def get_ticket_status(self) -> int:
        """
        Returns if ticket system is already set up.

        Returns:
            Status (bool): The ticket system status.
        """
        return self._load_ticket_config()[self.TICKET_CONFIG_STATUS_KEY]
    
    def set_ticket_status(self, status: bool) -> int:
        """
        Set if ticket system is set up or not.

        Args:
            Status (bool): The ticket system status.
        """
        self.ticket_config[self.TICKET_CONFIG_STATUS_KEY] = status
        self._update_ticket_config()
