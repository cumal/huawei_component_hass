"""Example of a custom component exposing a service."""
from __future__ import annotations

import logging

from datetime import timedelta
import requests
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.typing import ConfigType
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "huawei_service_sync"
_LOGGER = logging.getLogger(__name__)

CONF_URL = "url"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_URL): cv.string,
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

def create_session():
    session = requests.Session()
    session.verify = False
    return session

class HuaweiDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Huawei Router data."""

    def __init__(self, hass, entry):
        """Initialize."""
        self.entry = entry
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        def _fetch():
            url = self.entry.data[CONF_URL]
            username = self.entry.data[CONF_USERNAME]
            password = self.entry.data[CONF_PASSWORD]
            scheme, host = url.split("://", 1) if "://" in url else ("http", url)
            
            session = create_session()
            with Connection(f"{scheme}://{username}:{password}@{host}/", requests_session=session) as connection:
                client = Client(connection)
                return {
                    "device_information": client.device.information(),
                    "dhcp_settings": client.dhcp.settings(),
                    "device_signal": client.device.signal(),
                    "monitoring_status": client.monitoring.status(),
                    "traffic_statistics": client.monitoring.traffic_statistics(),
                    "lan_host_info": client.lan.host_info(),
                }

        try:
            return await self.hass.async_add_executor_job(_fetch)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    coordinator = HuaweiDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Register services if not already registered (using the first entry's config)
    if not hass.services.has_service(DOMAIN, 'get_info'):
        _register_services(hass, entry.data)

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "text", "button"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor", "text", "button"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

def _register_services(hass: HomeAssistant, conf: dict):
    def get_client():
        url = conf[CONF_URL]
        username = conf[CONF_USERNAME]
        password = conf[CONF_PASSWORD]
        scheme, host = url.split("://", 1) if "://" in url else ("http", url)
        session = create_session()
        with Connection(f"{scheme}://{username}:{password}@{host}/", requests_session=session) as connection:
            return Client(connection)

    async def get_info(call: ServiceCall) -> None:
        """Get router information."""
        def _fetch():
            with get_client() as client:
                info = client.device.information()
                _LOGGER.info("Router Information: %s", info)
                hass.components.persistent_notification.create(
                    f"Device: {info.get('DeviceName')}\nSW: {info.get('SoftwareVersion')}",
                    title="Huawei Router Info"
                )
        await hass.async_add_executor_job(_fetch)

    # Register our service with Home Assistant.
    hass.services.async_register(DOMAIN, 'get_info', get_info)

def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the sync service example component."""
    # Return true to allow UI setup
    return True
