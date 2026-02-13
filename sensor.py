"""Platform for router integration."""
from __future__ import annotations

import logging
import requests

from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from . import DOMAIN, create_session

_LOGGER = logging.getLogger(__name__)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    # Legacy setup not supported with coordinator in this example
    pass

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    config = entry.data
    async_add_entities([
        LocalRouter(coordinator, config),
        RouterDHCPSettings(coordinator, config),
        RouterDNSSettings(coordinator, config),
        RouterSignalSensor(coordinator, config),
        RouterMonitoringStatus(coordinator, config),
    ])

class LocalRouter(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Huawei Router"
    _attr_icon = "mdi:router-wireless"

    def __init__(self, coordinator, config):
        super().__init__(coordinator)
        self._config = config
        self._attr_extra_state_attributes = {}

    @property
    def unique_id(self):
        return f"{self._config['url']}_sensor"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._config["url"])},
            "name": "Huawei Router",
            "manufacturer": "Huawei",
            "model": "LTE",
            "sw_version": self._attr_extra_state_attributes.get("SoftwareVersion") if self._attr_extra_state_attributes else None,
        }

    @property
    def native_value(self):
        return self.coordinator.data.get("device_information", {}).get("DeviceName", "Unknown")

    @property
    def extra_state_attributes(self):
        return self.coordinator.data.get("device_information", {})

class RouterDHCPSettings(CoordinatorEntity, SensorEntity):
    """Representation of a DHCP Settings Sensor."""

    _attr_name = "Router DHCP Settings"
    _attr_icon = "mdi:ip-network"

    def __init__(self, coordinator, config):
        super().__init__(coordinator)
        self._config = config
        self._attr_extra_state_attributes = {}

    @property
    def unique_id(self):
        return f"{self._config['url']}_dhcp_settings"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._config["url"])},
            "name": "Huawei Router",
            "manufacturer": "Huawei",
            "model": "LTE",
        }

    @property
    def native_value(self):
        return self.coordinator.data.get("dhcp_settings", {}).get("DhcpIPAddress", "Unknown")

    @property
    def extra_state_attributes(self):
        return self.coordinator.data.get("dhcp_settings", {})

class RouterSignalSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Signal Sensor."""

    _attr_name = "Router Signal"
    _attr_icon = "mdi:signal"

    def __init__(self, coordinator, config):
        super().__init__(coordinator)
        self._config = config
        self._attr_extra_state_attributes = {}

    @property
    def unique_id(self):
        return f"{self._config['url']}_signal"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._config["url"])},
            "name": "Huawei Router",
            "manufacturer": "Huawei",
            "model": "LTE",
        }

    @property
    def native_value(self):
        return self.coordinator.data.get("device_signal", {}).get("rssi", "Unknown")

    @property
    def extra_state_attributes(self):
        return self.coordinator.data.get("device_signal", {})

class RouterMonitoringStatus(CoordinatorEntity, SensorEntity):
    """Representation of a Monitoring Status Sensor."""

    _attr_name = "Router Monitoring Status"
    _attr_icon = "mdi:monitor-dashboard"

    def __init__(self, coordinator, config):
        super().__init__(coordinator)
        self._config = config
        self._attr_extra_state_attributes = {}

    @property
    def unique_id(self):
        return f"{self._config['url']}_monitoring_status"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._config["url"])},
            "name": "Huawei Router",
            "manufacturer": "Huawei",
            "model": "LTE",
        }

    @property
    def native_value(self):
        return self.coordinator.data.get("monitoring_status", {}).get("ConnectionStatus", "Unknown")

    @property
    def extra_state_attributes(self):
        return self.coordinator.data.get("monitoring_status", {})

class RouterDNSSettings(CoordinatorEntity, SensorEntity):
    """Representation of a DNS Settings Sensor."""

    _attr_name = "Router DNS Settings"
    _attr_icon = "mdi:dns"

    def __init__(self, coordinator, config):
        super().__init__(coordinator)
        self._config = config
        self._attr_extra_state_attributes = {}

    @property
    def unique_id(self):
        return f"{self._config['url']}_dns_settings"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._config["url"])},
            "name": "Huawei Router",
            "manufacturer": "Huawei",
            "model": "LTE",
        }

    @property
    def native_value(self):
        data = self.coordinator.data.get("dhcp_settings", {})
        return f"{data.get('PrimaryDns', 'Unknown')}, {data.get('SecondaryDns', 'Unknown')}"

    @property
    def extra_state_attributes(self):
        return self.coordinator.data.get("dhcp_settings", {})
