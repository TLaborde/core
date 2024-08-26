"""Representation of an Ichijo Energy sensor."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import IchijoEnergyDataUpdateCoordinator


class IchijoEnergySensor(
    CoordinatorEntity[IchijoEnergyDataUpdateCoordinator], SensorEntity
):
    """Representation of an Ichijo Energy sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: IchijoEnergyDataUpdateCoordinator,
        sensor_type: str,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"
        self._attr_name = f"{sensor_type.replace('_', ' ').title()}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this entity."""
        return DeviceInfo(
            identifiers={(DOMAIN, "id" + str(self._attr_unique_id))},
            name="Ichijo Energy Device",
            manufacturer="Ichijo",
            # Add more device info as needed
        )

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._sensor_type)

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement."""
        if self._sensor_type == "energy_consumption":
            return "W"
        if self._sensor_type == "battery_state":
            return "%"
        if self._sensor_type == "solar_output":
            return "W"
        return None

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the device class of the sensor."""
        if self._sensor_type == "energy_consumption":
            return SensorDeviceClass.POWER
        if self._sensor_type == "battery_state":
            return SensorDeviceClass.BATTERY
        if self._sensor_type == "solar_output":
            return SensorDeviceClass.POWER
        return None

    @property
    def state_class(self) -> SensorStateClass | None:
        """Return the state class of the sensor."""
        if self._sensor_type in ["energy_consumption", "solar_output", "battery_state"]:
            return SensorStateClass.MEASUREMENT
        return None
