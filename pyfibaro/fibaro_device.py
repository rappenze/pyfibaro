"""Endpoint object to access the endpoint settings/info"""
from __future__ import annotations

import logging
from typing import Any

from .common.const import IGNORE_DEVICE
from .common.rest_client import RestClient

_LOGGER = logging.getLogger(__name__)


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
        if arguments:
            args_prepared = {"args": arguments}
            _LOGGER.debug(
                "Execute %s for device %s with args %s.",
                action,
                self.fibaro_id,
                args_prepared,
            )
            return self._rest_client.post(url, json=args_prepared)

        _LOGGER.debug("Execute %s for device %s without args.", action, self.fibaro_id)
        return self._rest_client.post(url)

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
