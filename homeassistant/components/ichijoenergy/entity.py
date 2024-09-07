"""IchijoEnergy base entity."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from . import IchijoEnergyData
from .const import DOMAIN


class IchijoEnergyEntity(Entity):
    """Defines a base IchijoEnergy entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        data: IchijoEnergyData,
    ) -> None:
        """Initialize the IchijoEnergy entity."""
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, data.device_id)},
            serial_number=data.device_id,
            manufacturer="IchijoEnergy",
            model="EZ1-M",
        )
