"""Config flow for Hello World integration."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_NAME, CONF_PATH, CONF_URL, CONF_SCAN_INTERVAL
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN  # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)
CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SCAN_INTERVAL): cv.positive_int,
    }
)

class CustomFlow(config_entries.ConfigFlow, domain=DOMAIN):
    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        errors: Dict[str, str] = {}
        if user_input is not None:
            self.data = user_input
            return self.async_create_entry(title="Test Integration", data=self.data)

        return self.async_show_form(step_id="user", data_schema=CONFIG_SCHEMA, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handles options flow for the component."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        errors: Dict[str, str] = {}
        if user_input is not None:
            self.data = user_input
            return self.async_create_entry(title="Test Integration", data=self.data)

        return self.async_show_form(step_id="init", data_schema=CONFIG_SCHEMA, errors=errors)
