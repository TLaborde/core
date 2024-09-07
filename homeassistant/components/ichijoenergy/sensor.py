"""The read-only sensors for IchijoEnergy local API integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
    StateType,
)
from homeassistant.const import UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import IchijoEnergyConfigEntry, IchijoEnergyData
from .api import IchijoEnergyOutputData
from .coordinator import IchijoEnergyDataCoordinator
from .entity import IchijoEnergyEntity


@dataclass(frozen=True, kw_only=True)
class IchijoEnergyLocalApiSensorDescription(SensorEntityDescription):
    """Describes Ichijo Energy sensor entity."""

    value_fn: Callable[[IchijoEnergyOutputData], float | None]


SENSORS: tuple[IchijoEnergyLocalApiSensorDescription, ...] = (
    IchijoEnergyLocalApiSensorDescription(
        key="solar_power",
        translation_key="solar_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda c: c.solar,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="battery_power",
        translation_key="battery_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda c: c.battery,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="home_consumption",
        translation_key="home_consumption",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda c: c.home,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="grid_use",
        translation_key="grid_use",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda c: c.grid,
    ),
    # IchijoEnergyLocalApiSensorDescription(
    #    key="grid_power",
    #    translation_key="grid_power",
    #    native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    #    device_class=SensorDeviceClass.ENERGY,
    #    state_class=SensorStateClass.TOTAL_INCREASING,
    #    value_fn=lambda c: c.te1 + c.te2,
    # ),
    # IchijoEnergyLocalApiSensorDescription(
    #    key="lifetime_production_p1",
    #    translation_key="lifetime_production_p1",
    #    native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    #    device_class=SensorDeviceClass.ENERGY,
    #    state_class=SensorStateClass.TOTAL_INCREASING,
    #    value_fn=lambda c: c.te1,
    # ),
    # IchijoEnergyLocalApiSensorDescription(
    #    key="lifetime_production_p2",
    #    translation_key="lifetime_production_p2",
    #    native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    #    device_class=SensorDeviceClass.ENERGY,
    #    state_class=SensorStateClass.TOTAL_INCREASING,
    #    value_fn=lambda c: c.te2,
    # ),
    # IchijoEnergyLocalApiSensorDescription(
    #    key="today_production",
    #    translation_key="today_production",
    #    native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    #    device_class=SensorDeviceClass.ENERGY,
    #    state_class=SensorStateClass.TOTAL_INCREASING,
    #    value_fn=lambda c: c.e1 + c.e2,
    # ),
    # IchijoEnergyLocalApiSensorDescription(
    #    key="today_production_p1",
    #    translation_key="today_production_p1",
    #    native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    #    device_class=SensorDeviceClass.ENERGY,
    #    state_class=SensorStateClass.TOTAL_INCREASING,
    #    value_fn=lambda c: c.e1,
    # ),
    # IchijoEnergyLocalApiSensorDescription(
    #    key="today_production_p2",
    #    translation_key="today_production_p2",
    #    native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    #    device_class=SensorDeviceClass.ENERGY,
    #    state_class=SensorStateClass.TOTAL_INCREASING,
    #    value_fn=lambda c: c.e2,
    # ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: IchijoEnergyConfigEntry,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    config = config_entry.runtime_data

    add_entities(
        IchijoEnergySensorWithDescription(
            data=config,
            entity_description=desc,
        )
        for desc in SENSORS
    )


class IchijoEnergySensorWithDescription(
    CoordinatorEntity[IchijoEnergyDataCoordinator], IchijoEnergyEntity, SensorEntity
):
    """Base sensor to be used with description."""

    entity_description: IchijoEnergyLocalApiSensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        data: IchijoEnergyData,
        entity_description: IchijoEnergyLocalApiSensorDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(data.coordinator)
        IchijoEnergyEntity.__init__(self, data)
        self.entity_description = entity_description
        self._attr_unique_id = f"{data.device_id}_{entity_description.key}"

    @property
    def native_value(self) -> StateType:
        """Return value of sensor."""
        return self.entity_description.value_fn(self.coordinator.data.output_data)
