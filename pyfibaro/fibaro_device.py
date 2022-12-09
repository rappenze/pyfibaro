"""Endpoint object to access the endpoint settings/info"""
from __future__ import annotations

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
        return int(self.raw_data.get("id", 0))

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
        """Returns the battery level of the device."""
        return int(self.properties.get("batteryLevel", 0))

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
    def value(self) -> ValueModel:
        """Returns the value info."""
        return ValueModel(self.properties, "value")

    @property
    def value_2(self) -> ValueModel:
        """Returns the value info."""
        return ValueModel(self.properties, "value2")

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

        devices: list[DeviceModel] = []
        for device in raw_data:
            if device.get("type") in IGNORE_DEVICE:
                _LOGGER.debug("Ignore device: %s", device.get("id"))
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
        If no default is set, a  TypeError is raised for invalid values.
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
                return value.lower() == "true"
            if isinstance(value, (int, float)):
                return value != 0
            raise TypeError(f"Value cannot be converted to bool {value}")
        except TypeError as ex:
            if default is None:
                raise ex
            return default
