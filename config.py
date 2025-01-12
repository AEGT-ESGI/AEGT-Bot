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
    TICKET_CONFIG_CHANNEL_ID_KEY = "CHANNEL_ID"
    TICKET_CONFIG_CATEGORY_ID_KEY = "CATEGORY_ID"
    TICKET_CONFIG_ROLE_ID_KEY = "ROLE_ID"

    def __init__(self) -> None:
        self.config = Config()
        self._load_ticket_config()

    def _load_ticket_config(self) -> Dict:
        self.ticket_config = self.config.get_config()[self.TICKET_CONFIG_KEY]
        return self.ticket_config

    def _update_ticket_config(self) -> None:
        self.config.set_config(self.TICKET_CONFIG_KEY, self.ticket_config)

    def get_ticket_channel(self) -> int:
        """
        Returns the ID channel where ticket system was set up.

        Returns:
            Int: The ID channel where ticket system was set up.
        """
        return self._load_ticket_config()[self.TICKET_CONFIG_CHANNEL_ID_KEY]
    
    def get_ticket_category(self) -> int:
        """
        Returns the ID category where tickets will be created.

        Returns:
            Int: The ID category where tickets will be created.
        """
        return self._load_ticket_config()[self.TICKET_CONFIG_CATEGORY_ID_KEY]
    
    def get_ticket_role(self) -> int:
        """
        Returns the ID ticket role which is added to ticket channel for support.

        Returns:
            Int: The ID ticket role which is added to ticket channel for support.
        """
        return self._load_ticket_config()[self.TICKET_CONFIG_ROLE_ID_KEY]

    def set_ticket_channel(self, channel_id: int) -> None:
        """
        Sets the ID for the channel where system ticket will be set up.
        Args:
            channel_id (int): The ID of the channel
        """
        self.ticket_config[self.TICKET_CONFIG_CHANNEL_ID_KEY] = channel_id
        self._update_ticket_config()

    def set_ticket_category(self, category_id: int) -> None:
        """
        Sets the ID for the category where tickets will be created.

        Args:
            category_id (int): The ID of the category
        """
        self.ticket_config[self.TICKET_CONFIG_CATEGORY_ID_KEY] = category_id
        self._update_ticket_config()

    def set_ticket_role(self, role_id: int) -> None:
        """
        Sets the ID for the role that will be added to the ticket channel for support.
        Args:
            role_id (int): The ID of the role
        """
        self.ticket_config[self.TICKET_CONFIG_ROLE_ID_KEY] = role_id
        self._update_ticket_config()
