from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from . import DOMAIN, CONF_URL, CONF_USERNAME, CONF_PASSWORD

class HuaweiServiceSyncConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Huawei Service Sync."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Huawei Router", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_URL): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            })
        )
    
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return HuaweiServiceSyncOptionsFlow(config_entry)

class HuaweiServiceSyncOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Huawei Service Sync."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional("primary_dns", default=self.config_entry.options.get("primary_dns", "")): str,
                vol.Optional("secondary_dns", default=self.config_entry.options.get("secondary_dns", "")): str,
            })
        )