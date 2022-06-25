"""Platform for sensor integration."""
from __future__ import annotations

import datetime
from datetime import timedelta

from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant import config_entries
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from custom_components.ha_test_integration.const import DOMAIN
import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    config = hass.data[DOMAIN][config_entry.entry_id]
    SCAN_INTERVAL = 300
    if config_entry.options:
        config.update(config_entry.options)
        if 'scan_interval' in config.options:
            SCAN_INTERVAL = config.options["scan_interval"]
    if 'scan_interval' in config:
        SCAN_INTERVAL = config["scan_interval"]
    async_add_entities([IPSensor(SCAN_INTERVAL, False), IPSensor(SCAN_INTERVAL, True)], update_before_add=True)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    SCAN_INTERVAL = 300
    if 'scan_interval' in config:
        SCAN_INTERVAL = config["scan_interval"]
    async_add_entities([IPSensor(SCAN_INTERVAL, False), IPSensor(SCAN_INTERVAL, True)], update_before_add=True)



class IPSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, scan_interval: int, ipv6: bool):
        self.ipv6 = ipv6
        self._attr_icon = 'mdi:web'
        self._attr_name = "Public IPv4"
        self._attr_unique_id = "publicipv4"
        if (self.ipv6):
            self._attr_name = "Public IPv6"
            self._attr_unique_id = "publicipv6"
        self._attr_scan_interval = timedelta(seconds=scan_interval)

    async def async_update(self) -> None:
        _LOGGER.warning(f"Updating IP sensor: {datetime.datetime.now()}")
        if (self.ipv6):
            url = 'https://api64.ipify.org/?format=json'
        else:
            url = 'https://api.ipify.org/?format=json'



        """call the url using aiohttp and extract ip from result"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self._attr_native_value = data['ip']
                    self._state = None
                else:
                    self._state = "Error"
                    _LOGGER.error("Error getting IP")
