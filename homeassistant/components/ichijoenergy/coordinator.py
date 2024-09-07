"""The coordinator for IchijoEnergy local API integration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import IchijoEnergyAPI, IchijoEnergyOutputData
from .const import LOGGER


@dataclass
class IchijoEnergySensorData:
    """Representing different IchijoEnergy sensor data."""

    output_data: IchijoEnergyOutputData


class IchijoEnergyDataCoordinator(DataUpdateCoordinator[IchijoEnergySensorData]):
    """Coordinator used for all sensors."""

    def __init__(self, hass: HomeAssistant, api: IchijoEnergyAPI) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            LOGGER,
            name="IchijoEnergy Data",
            update_interval=timedelta(seconds=12),
        )
        self.api = api

    async def _async_setup(self) -> None:
        # try:
        #    max_power = (await self.api.get_device_info()).maxPower
        # except (ConnectionError, TimeoutError):
        #    raise UpdateFailed from None
        # self.api.max_power = max_power
        pass

    async def _async_update_data(self) -> IchijoEnergySensorData:
        output_data = await self.api.get_output_data()
        return IchijoEnergySensorData(output_data=output_data)
