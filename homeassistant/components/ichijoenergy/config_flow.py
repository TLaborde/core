"""Config flow for Ichijo Energy."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow

from .api import IchijoEnergyAPI
from .const import DOMAIN


async def _async_has_devices(hass: HomeAssistant) -> bool:
    """Return if there are devices that can be discovered."""
    return await hass.async_add_executor_job(IchijoEnergyAPI.discover)


config_entry_flow.register_discovery_flow(DOMAIN, "Ichijo Energy", _async_has_devices)
