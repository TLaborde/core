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
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfEnergy, UnitOfPower
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
        key="power_production",
        translation_key="power_production",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        suggested_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda c: c.power_production,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_production_today",
        translation_key="energy_production_today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda c: c.energy_production_today,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_production_month",
        translation_key="energy_production_month",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda c: c.energy_production_month,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_production_total",
        translation_key="energy_production_total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_fn=lambda c: c.energy_production_total,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="power_export",
        translation_key="power_export",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        suggested_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda c: c.power_export,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_export_today",
        translation_key="energy_export_today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda c: c.energy_export_today,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_export_month",
        translation_key="energy_export_month",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda c: c.energy_export_month,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_export_total",
        translation_key="energy_export_total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_fn=lambda c: c.energy_export_total,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="power_import",
        translation_key="power_import",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        suggested_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda c: c.power_import,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_import_today",
        translation_key="energy_import_today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda c: c.energy_import_today,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_import_month",
        translation_key="energy_import_month",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda c: c.energy_import_month,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_import_total",
        translation_key="energy_import_total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_fn=lambda c: c.energy_import_total,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="power_consumption",
        translation_key="power_consumption",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        suggested_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda c: c.power_consumption,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_consumption_today",
        translation_key="energy_consumption_today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda c: c.energy_consumption_today,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_consumption_month",
        translation_key="energy_consumption_month",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda c: c.energy_consumption_month,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_consumption_total",
        translation_key="energy_consumption_total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_fn=lambda c: c.energy_consumption_total,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="power_charge",
        translation_key="power_charge",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        suggested_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda c: c.power_charge,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_power_charge_today",
        translation_key="energy_power_charge_today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda c: c.energy_power_charge_today,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_power_charge_month",
        translation_key="energy_power_charge_month",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda c: c.energy_power_charge_month,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_power_charge_total",
        translation_key="energy_power_charge_total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_fn=lambda c: c.energy_power_charge_total,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="power_discharge",
        translation_key="power_discharge",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        suggested_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda c: c.power_discharge,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_power_discharge_today",
        translation_key="energy_power_discharge_today",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda c: c.energy_power_discharge_today,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_power_discharge_month",
        translation_key="energy_power_discharge_month",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda c: c.energy_power_discharge_month,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="energy_power_discharge_total",
        translation_key="energy_power_discharge_total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        value_fn=lambda c: c.energy_power_discharge_total,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="performance_ratio",
        translation_key="performance_ratio",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda c: c.performance_ratio,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="self_sufficiency_today",
        translation_key="self_sufficiency_today",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda c: c.self_sufficiency_today,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="self_sufficiency_month",
        translation_key="self_sufficiency_month",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda c: c.self_sufficiency_month,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="self_sufficiency_total",
        translation_key="self_sufficiency_total",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda c: c.self_sufficiency_total,
    ),
    IchijoEnergyLocalApiSensorDescription(
        key="battery_level",
        device_class=SensorDeviceClass.BATTERY,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda battery: battery.battery_level,
    ),
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
