"""Data update coordinator for Ichijo Energy."""

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class IchijoEnergyDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Ichijo Energy data."""

    def __init__(self, hass: HomeAssistant, api) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),  # Adjust as needed
        )
        self.api = api

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            return await self.api.get_data()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
