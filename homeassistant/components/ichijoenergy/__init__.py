"""The Ichijo Energy integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .api import IchijoEnergyApi
from .const import DOMAIN
from .coordinator import IchijoEnergyDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Ichijo Energy from a config entry."""
    # Create API instance
    # Replace this with your actual API class
    api = IchijoEnergyApi(
        host=entry.data["host"],
        username=entry.data["username"],
        password=entry.data["password"],
    )

    # Create and store an update coordinator
    coordinator = IchijoEnergyDataUpdateCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
