"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant import config_entries
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from const import DOMAIN
import httpx

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    config = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([IPSensor(False), IPSensor(True)])

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    async_add_entities([IPSensor(False), IPSensor(True)])



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
        client = httpx.AsyncClient()
        if (self.ipv6):
            r = await client.get('https://api64.ipify.org/?format=json')
        else:
            r = await client.get('https://api.ipify.org/?format=json')
        await client.aclose()
        ip = str(r.json()['ip'])
        self._attr_native_value = ip