from __future__ import annotations
import logging
from homeassistant.components.button import ButtonEntity
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from . import DOMAIN, create_session

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the button platform from a config entry."""
    config = entry.data
    async_add_entities([RouterRebootButton(config)])

class RouterRebootButton(ButtonEntity):
    _attr_name = "Reboot Router"
    _attr_icon = "mdi:restart"

    def __init__(self, config):
        self._config = config

    @property
    def unique_id(self):
        return f"{self._config['url']}_reboot_button"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._config["url"])},
            "name": "Huawei Router",
            "manufacturer": "Huawei",
            "model": "LTE",
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        def _reboot():
            url = self._config["url"]
            username = self._config["username"]
            password = self._config["password"]
            scheme, host = url.split("://", 1) if "://" in url else ("http", url)
            
            session = create_session()
            with Connection(f"{scheme}://{username}:{password}@{host}/", requests_session=session) as connection:
                client = Client(connection)
                client.device.reboot()
        
        await self.hass.async_add_executor_job(_reboot)