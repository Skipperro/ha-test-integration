"""Platform for sensor integration."""
from __future__ import annotations
from datetime import timedelta

from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant import config_entries
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity_registry import async_get, async_entries_for_config_entry
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from custom_components.ha_test_integration.const import DOMAIN
import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=300)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    _LOGGER.warning("async_setup_entry")
    config = hass.data[DOMAIN][config_entry.entry_id]
    if config_entry.options:
        config.update(config_entry.options)
    to_add = []
    if 'check_ipv4' in config:
        if config['check_ipv4']:
            to_add.append(IPSensor(False))
    if 'check_ipv6' in config:
        if config['check_ipv6']:
            to_add.append(IPSensor(True))

    entity_registry = async_get(hass)
    entries = async_entries_for_config_entry(
        entity_registry, config_entry.entry_id
    )
    for entry in entries:
        entity_registry.async_remove(entry.entity_id)

    async_add_entities(to_add, update_before_add=True)

"""
async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    _LOGGER.warning("async_setup_platform")
    to_add = []
    if 'check_ipv4' in config:
        if config['check_ipv4']:
            to_add.append(IPSensor(False))
    if 'check_ipv6' in config:
        if config['check_ipv6']:
            to_add.append(IPSensor(True))

    async_add_entities(to_add, update_before_add=True)
"""

class IPSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, ipv6: bool):
        self.ipv6 = ipv6
        self._attr_icon = 'mdi:web'
        self._attr_name = "Public IPv4"
        self._attr_unique_id = "publicipv4"
        if (self.ipv6):
            self._attr_name = "Public IPv6"
            self._attr_unique_id = "publicipv6"

    async def async_update(self) -> None:
        if (self.ipv6):
            url = 'https://api64.ipify.org/?format=json'
        else:
            url = 'https://api.ipify.org/?format=json'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self._attr_native_value = data['ip']
                    self._state = None
                else:
                    self._state = "Error"
                    _LOGGER.error("Error getting IP")
