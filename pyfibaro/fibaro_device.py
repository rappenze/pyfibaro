"""Endpoint object to access the endpoint settings/info"""
from __future__ import annotations

import json
import logging
from typing import Any

from .common.const import IGNORE_DEVICE
from .common.rest_client import RestClient

_LOGGER = logging.getLogger(__name__)


def _to_bool(bool_value: bool | str) -> bool:
    """Convert any value to bool."""
    if bool_value is not None:
        if isinstance(bool_value, bool):
            return bool_value
        if isinstance(bool_value, str):
            return bool_value.lower() == "true"
    return False


class DeviceModel:
    """Model of a device."""

    def __init__(self, data: dict, rest_client: RestClient, api_version: int) -> None:
        """Constructor."""
        self.raw_data = data
        self._rest_client = rest_client
        self._api_version = api_version

    @property
    def fibaro_id(self) -> int:
        """Device id"""
        return self.raw_data.get("id")

    @property
    def name(self) -> str:
        """Device name"""
        return self.raw_data.get("name")

    @property
    def parent_fibaro_id(self) -> int:
        """Id of the parent device or 0 if there is no parent."""
        return int(self.raw_data.get("parentId", 0))

    @property
    def type(self) -> str | None:
        """Device type."""
        return self.raw_data.get("type")

    @property
    def base_type(self) -> str | None:
        """Device base type."""
        return self.raw_data.get("baseType")

    @property
    def room_id(self) -> int:
        """Room id of the device or 0 if no room is assigned."""
        return int(self.raw_data.get("roomID", 0))

    @property
    def properties(self) -> dict:
        """Get the properties."""
        return self.raw_data.get("properties", {})

    @property
    def actions(self) -> dict[str, int]:
        """Get the available actions."""
        return self.raw_data.get("actions", {})

    def has_interface(self, interface_name: str) -> bool:
        """Returns True if the device has the according interface defined.

        Interfaces are capabilities of the device.
        """
        return interface_name in self.raw_data.get("interfaces", [])

    @property
    def unit(self) -> str | None:
        """Returns the unit of the devices value attribute or None."""
        return self.properties.get("unit")

    @property
    def has_unit(self) -> bool:
        """Returns true if the device has a unit property."""
        return "unit" in self.properties

    @property
    def endpoint_id(self) -> int:
        """Returns the endpoint id or 0 if there is no endpoint id.

        Endpoints are numbered if one physical device exposes different endpoints.
        """
        return int(self.properties.get("endPointId", 0))

    @property
    def has_endpoint_id(self) -> bool:
        """Returns true if the device has a unit property."""
        return "endPointId" in self.properties

    @property
    def enabled(self) -> bool:
        """Returns the enabled flag of the device.

        If the device does not support that flag, True is returned.
        """
        return self.raw_data.get("enabled", True)

    @property
    def visible(self) -> bool:
        """Returns the visible state of the device."""
        return self.raw_data.get("visible", True)

    @property
    def is_plugin(self) -> bool:
        """Returns the device type.

        Returns:
        True for virtual devices and Quick Apps
        False for physical devices and controllers
        """
        return self.raw_data.get("isPlugin", True)

    @property
    def battery_level(self) -> int:
        """Returns the battery level of the device in percent."""
        percent = int(self.properties.get("batteryLevel", 0))
        return 0 if percent == 255 else percent

    @property
    def has_battery_level(self) -> bool:
        """Returns true if the device has a unit property."""
        return "batteryLevel" in self.properties

    @property
    def armed(self) -> bool:
        """Returns the armed state of the device if supported,
        otherwise False is returned.
        """
        return _to_bool(self.properties.get("armed", False))

    @property
    def has_armed(self) -> bool:
        """Returns true if the device has a unit property."""
        return "armed" in self.properties

    @property
    def dead(self) -> bool:
        """Returns the state if the device is reachable if supported,
        otherwise False is returned.
        """
        return _to_bool(self.properties.get("dead", False))

    @property
    def has_dead(self) -> bool:
        """Returns true if the device has a dead property."""
        return "dead" in self.properties

    @property
    def dead_reason(self) -> str | None:
        """Returns the dead reason or None if not supported."""
        return self.properties.get("deadReason")

    @property
    def has_dead_reason(self) -> bool:
        """Returns true if the device has a deadReason property."""
        return "deadReason" in self.properties

    @property
    def value(self) -> ValueModel:
        """Returns the value info."""
        return ValueModel(self.properties, "value")

    @property
    def value_2(self) -> ValueModel:
        """Returns the value info."""
        return ValueModel(self.properties, "value2")

    @property
    def state(self) -> ValueModel:
        """Returns the state info."""
        return ValueModel(self.properties, "state")

    @property
    def color(self) -> ColorModel:
        """Returns the color info."""
        return ColorModel(self.properties, "color")

    @property
    def last_color_set(self) -> ColorModel:
        """Returns the last set color info."""
        return ColorModel(self.properties, "lastColorSet")

    @property
    def brightness(self) -> int:
        """Returns the brightness of the device. If missing, 0 is returned."""
        return int(self.properties.get("brightness", 0))

    @property
    def has_brightness(self) -> bool:
        """Returns true if the device has a brightness property."""
        return "brightness" in self.properties

    @property
    def current_program(self) -> int:
        """Returns the current program of the device or None."""
        return int(self.properties.get("currentProgram", 0))

    @property
    def current_program_id(self) -> int:
        """Returns the current pogram id of the device or 0."""
        return int(self.properties.get("currentProgramID", 0))

    @property
    def mode(self) -> int:
        """Returns the mode or 0 if there is no mode."""
        return int(self.properties.get("mode", 0))

    @property
    def has_mode(self) -> bool:
        """Returns true if the device has a mode."""
        return "mode" in self.properties

    @property
    def supported_modes(self) -> list[int]:
        """Returns the supported modes, for example for fan or hvac devices."""
        if "supportedModes" in self.properties:
            modes = self.properties.get("supportedModes")
            if isinstance(modes, str) and modes != "":
                return [int(mode) for mode in modes.split(",")]
            if isinstance(modes, list):
                return [int(mode) for mode in modes]
        return []

    @property
    def has_supported_modes(self) -> bool:
        """Returns true if the device has a supported modes property."""
        return "supportedModes" in self.properties

    @property
    def operating_mode(self) -> int:
        """Returns the operating mode or 0 if there is no operating mode."""
        return int(self.properties.get("operatingMode", 0))

    @property
    def has_operating_mode(self) -> bool:
        """Returns true if the device has a operating mode."""
        return "operatingMode" in self.properties

    @property
    def supported_operating_modes(self) -> list[int]:
        """Returns the supported operating modes, for example for fan or hvac devices."""
        if "supportedOperatingModes" in self.properties:
            modes = self.properties.get("supportedOperatingModes")
            if isinstance(modes, str) and modes != "":
                return [int(mode) for mode in modes.split(",")]
            if isinstance(modes, list):
                return [int(mode) for mode in modes]
        return []

    @property
    def has_supported_operating_modes(self) -> bool:
        """Returns true if the device has a supported operating modes property."""
        return "supportedOperatingModes" in self.properties

    @property
    def thermostat_mode(self) -> str | None:
        """Returns the thermostat mode or None if there is no thermostat mode."""
        return self.properties.get("thermostatMode")

    @property
    def has_thermostat_mode(self) -> bool:
        """Returns true if the device has a thermostat mode."""
        return "thermostatMode" in self.properties

    @property
    def thermostat_operating_state(self) -> str | None:
        """Returns the thermostat operating state or None if there
        is no thermostat operating state.
        """
        return self.properties.get("thermostatOperatingState")

    @property
    def has_thermostat_operating_state(self) -> bool:
        """Returns true if the device has a thermostat operating state."""
        return "thermostatOperatingState" in self.properties

    @property
    def supported_thermostat_modes(self) -> list[str]:
        """Returns the supported thermostat modes, for example for hvac devices."""
        if "supportedThermostatModes" in self.properties:
            return self.properties.get("supportedThermostatModes")
        return []

    @property
    def has_supported_thermostat_modes(self) -> bool:
        """Returns true if the device has a supported thermostat modes property."""
        return "supportedThermostatModes" in self.properties

    @property
    def heating_thermostat_setpoint(self) -> float:
        """Returns the heating thermostat setpoint or 0 if there is no value."""
        return float(self.properties.get("heatingThermostatSetpoint", 0.0))

    @property
    def has_heating_thermostat_setpoint(self) -> bool:
        """Returns true if the device has a heating thermostat setpoint property."""
        return "heatingThermostatSetpoint" in self.properties

    @property
    def heating_thermostat_setpoint_future(self) -> float:
        """Returns the heating thermostat setpoint future or 0 if there is no value."""
        return float(self.properties.get("heatingThermostatSetpointFuture", 0.0))

    @property
    def has_heating_thermostat_setpoint_future(self) -> bool:
        """Returns true if the device has a heating thermostat setpoint future property."""
        return "heatingThermostatSetpointFuture" in self.properties

    @property
    def target_level(self) -> float:
        """Returns the target level or 0 if there is no value."""
        return float(self.properties.get("targetLevel", 0.0))

    @property
    def has_central_scene_event(self) -> bool:
        """Returns true if the device can issue central scene events."""
        return "centralSceneSupport" in self.properties

    @property
    def central_scene_event(self) -> list[SceneEvent]:
        """Returns list of potential scene events."""
        central_scene_support = []
        value = self.properties.get("centralSceneSupport")
        if isinstance(value, list):
            central_scene_support = value
        if isinstance(value, str):
            central_scene_support = json.loads(value)

        result = []
        for central_scene in central_scene_support:
            key_id = int(central_scene.get("keyId"))
            key_attributes = central_scene.get("keyAttributes")
            result.append(SceneEvent(key_id, key_attributes))
        return result

    def execute_action(self, action: str, arguments: list[Any] | None = None) -> Any:
        """Execute a device action.

        Params:
        action: name of the action to call
        arguments: list of arguments needed for the action
        """
        if action not in self.actions:
            _LOGGER.warning(
                "The device %s has no action %s. Possible actions are %s",
                self.fibaro_id,
                action,
                self.actions,
            )

        url = f"devices/{self.fibaro_id}/action/{action}"

        args_prepared = {"args": arguments} if arguments else {}
        _LOGGER.debug(
            "Execute %s for device %s with args %s.",
            action,
            self.fibaro_id,
            args_prepared,
        )
        return self._rest_client.post(url, json=args_prepared)

    @staticmethod
    def read_devices(rest_client: RestClient, api_version: int) -> list[DeviceModel]:
        """Returns a list of devices."""
        raw_data: list[dict] = rest_client.get("devices")

        devices: list[dict] = []
        for device in raw_data:
            if device.get("type") in IGNORE_DEVICE:
                _LOGGER.debug("Ignore device: %s", device.get("id"))
            elif "id" not in device or "name" not in device:
                _LOGGER.debug(
                    "Ignore device because it does not contain id or name")
            else:
                devices.append(device)
        return [DeviceModel(data, rest_client, api_version) for data in devices]


class ValueModel:
    """Model to read out the value in several ways."""

    def __init__(self, properties: dict, property_name: str) -> None:
        """Constructor."""
        self._properties = properties
        self._property_name = property_name

    @property
    def has_value(self) -> bool:
        """Returns true if the device has a value property."""
        return self._property_name in self._properties

    @property
    def is_bool_value(self) -> bool:
        """Returns True if the device value property is a bool,
        either as string or real bool type.
        """
        if self.has_value:
            value = self._properties.get(self._property_name)
            if isinstance(value, bool):
                return True
            if isinstance(value, str):
                return value.lower() in ("true", "false")

        return False

    def str_value(self, default: str | None = None) -> str:
        """Returns the value converted to str or default if
        the object has no value.

        Raises:
        If no default is set, a TypeError is raised if no value exists.
        """
        if self.has_value:
            return str(self._properties.get(self._property_name, default))

        if default is None:
            raise TypeError("No value attribute available")
        return default

    def int_value(self, default: int | None = None) -> int:
        """Returns the value converted to int or default if
        conversion failes or the object has no value.

        Raises:
        If no default is set, a TypeError is raised for invalid values.
        """
        try:
            return int(float(self._properties.get(self._property_name)))
        except TypeError as ex:
            if default is None:
                raise ex
            return default

    def float_value(self, default: float | None = None) -> float:
        """Returns the value converted to float or default if
        conversion failes or the object has no value.

        Raises:
        If no default is set, a TypeError is raised for invalid values.
        """
        try:
            return float(self._properties.get(self._property_name))
        except TypeError as ex:
            if default is None:
                raise ex
            return default

    def bool_value(self, default: bool | None = None) -> bool:
        """Returns the value converted to bool or default if
        conversion failes or the object has no value.

        Raises:
        If no default is set, a TypeError is raised for invalid values.
        """
        try:
            value = self._properties.get(self._property_name)
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                if self.is_bool_value:
                    return value.lower() == "true"
                return self.float_value(0) != 0
            if isinstance(value, (int, float)):
                return value != 0
            raise TypeError(f"Value cannot be converted to bool {value}")
        except TypeError as ex:
            if default is None:
                raise ex
            return default

    def dict_value(self, default: dict | None = None) -> dict:
        """Returns the value converted to a dict or default if
        conversion failes or the object has no value.

        Raises:
        If no default is set, an error is raised for invalid values.
        """
        try:
            value = self._properties.get(self._property_name)
            if isinstance(value, dict):
                return value
            if isinstance(value, str):
                return json.loads(value)
            raise TypeError(f"Value cannot be converted to dict {value}")
        except TypeError as ex:
            if default is None:
                raise ex
            return default


class ColorModel:
    """Model to read out the color."""

    def __init__(self, properties: dict, property_name: str) -> None:
        """Constructor."""
        self._properties = properties
        self._property_name = property_name

    @property
    def has_color(self) -> bool:
        """Returns true if the device has a value property."""
        if self._property_name in self._properties:
            try:
                self.rgbw_color
                return True
            except TypeError:
                return False
        return False

    @property
    def rgbw_color(self) -> tuple[int, int, int, int]:
        """Returns the color as RGBW value.
        For RGB devices the white value is reported as 0.

        Raises:
        TypeError is raised for invalid values.
        """
        color = self._properties.get(self._property_name)
        if color is None:
            raise TypeError("Color is None.")
        rgbw = tuple(int(i) for i in color.split(","))
        if len(rgbw) != 4:
            raise TypeError(f"Color does not have 4 parts: {color}")
        return rgbw


class SceneEvent:
    """Model to read out the scene events."""

    def __init__(self, key_id: int, key_attributes: list[str]) -> None:
        """Constructor."""
        self._key_id = key_id
        self._key_attributes = key_attributes

    @property
    def key_id(self) -> int:
        """Returns the key id."""
        return self._key_id

    @property
    def key_event_types(self) -> list[str]:
        """Returns the possible key event types."""
        return self._key_attributes
