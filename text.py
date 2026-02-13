from __future__ import annotations
import logging
from homeassistant.components.text import TextEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from . import DOMAIN, create_session

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the text platform from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    config = entry.data
    async_add_entities([RouterPrimaryDNS(coordinator, config), RouterSecondaryDNS(coordinator, config)])

class RouterDNSEntity(CoordinatorEntity, TextEntity):
    """Base class for Router DNS Text Entities."""
    
    def __init__(self, coordinator, config):
        super().__init__(coordinator)
        self._config = config
        self._attr_has_entity_name = True

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._config["url"])},
            "name": "Huawei Router",
            "manufacturer": "Huawei",
            "model": "LTE",
        }

    def _get_connection(self):
        url = self._config["url"]
        username = self._config["username"]
        password = self._config["password"]
        scheme, host = url.split("://", 1) if "://" in url else ("http", url)
        session = create_session()
        return Connection(f"{scheme}://{username}:{password}@{host}/", requests_session=session)

    async def _async_update_settings(self, primary=None, secondary=None):
        def _do_update():
            with self._get_connection() as connection:
                client = Client(connection)
                # Fetch current to get IP and existing values
                current = client.dhcp.settings()
                router_ip = current.get('DhcpIPAddress')
                
                # Use provided value or fallback to current
                p_dns = primary if primary is not None else current.get('PrimaryDns')
                s_dns = secondary if secondary is not None else current.get('SecondaryDns')

                new_settings = {
                    'dhcp_ip_address': router_ip,
                    'dhcp_lan_netmask': "255.255.255.0",
                    'dhcp_status': True,
                    'dhcp_start_ip_range': 100,
                    'dhcp_end_ip_range': 200,
                    'dhcp_lease_time': 86400,
                    'dns_status': False,
                    'primary_dns': p_dns,
                    'secondary_dns': s_dns,
                    'show_dns_setting': True
                }
                client.dhcp.set_settings(**new_settings)
        
        await self.hass.async_add_executor_job(_do_update)
        await self.coordinator.async_request_refresh()

class RouterPrimaryDNS(RouterDNSEntity):
    _attr_name = "DNS Primary"
    _attr_icon = "mdi:server-network"

    @property
    def unique_id(self):
        return f"{self._config['url']}_primary_dns"

    @property
    def native_value(self):
        return self.coordinator.data.get("dhcp_settings", {}).get("PrimaryDns")

    async def async_set_value(self, value: str) -> None:
        await self._async_update_settings(primary=value)

class RouterSecondaryDNS(RouterDNSEntity):
    _attr_name = "DNS Secondary"
    _attr_icon = "mdi:server-network"

    @property
    def unique_id(self):
        return f"{self._config['url']}_secondary_dns"

    @property
    def native_value(self):
        return self.coordinator.data.get("dhcp_settings", {}).get("SecondaryDns")

    async def async_set_value(self, value: str) -> None:
        await self._async_update_settings(secondary=value)