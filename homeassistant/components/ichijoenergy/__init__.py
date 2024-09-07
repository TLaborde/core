"""The Ichijo Energy integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .api import IchijoEnergyAPI
from .coordinator import IchijoEnergyDataCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]


@dataclass
class IchijoEnergyData:
    """Store runtime data."""

    coordinator: IchijoEnergyDataCoordinator
    device_id: str


type IchijoEnergyConfigEntry = ConfigEntry[IchijoEnergyData]


async def async_setup_entry(
    hass: HomeAssistant, entry: IchijoEnergyConfigEntry
) -> bool:
    """Set up Ichijo Energy from a config entry."""

    api = IchijoEnergyAPI()
    coordinator = IchijoEnergyDataCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = IchijoEnergyData(
        coordinator=coordinator, device_id=(entry.unique_id or "uniq")
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
