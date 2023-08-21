"""Endpoint object to access the endpoint settings/info"""
from __future__ import annotations

import logging

from .common.rest_client import RestClient

_LOGGER = logging.getLogger(__name__)


class SceneModel:
    """Model of a scene."""

    def __init__(self, data: dict, rest_client: RestClient, api_version: int) -> None:
        """One scene."""
        self.raw_data = data
        self._rest_client = rest_client
        self._api_version = api_version

    @property
    def fibaro_id(self) -> int:
        """Scene id"""
        return self.raw_data.get("id")

    @property
    def name(self) -> str:
        """Scene name"""
        return self.raw_data.get("name")

    @property
    def room_id(self) -> int:
        """Room id of the scene or 0 if no room is assigned."""
        if self._api_version == 4:
            return int(self.raw_data.get("roomID", 0))
        else:
            return int(self.raw_data.get("roomId", 0))

    @property
    def visible(self) -> bool:
        """Returns the visible state of the scene."""
        if self._api_version == 4:
            return self.raw_data.get("visible", True)
        else:
            return not self.raw_data.get("hidden", False)

    def start(self, user_pin: str | None = None) -> None:
        """Start a scene."""
        if self._api_version == 4:
            if user_pin:
                raise NotImplementedError("Not supported on old fibaro hubs")
            self._send_action_v4("start")
        else:
            self._send_action_v5("execute", user_pin)

    def stop(self, user_pin: str | None = None) -> None:
        """Stop a scene."""
        if self._api_version == 4:
            if user_pin:
                raise NotImplementedError("Not supported on old fibaro hubs")
            self._send_action_v4("stop")
        else:
            self._send_action_v5("kill", user_pin)

    def _send_action_v4(self, action: str) -> None:
        url = f"scenes/{self.fibaro_id}/action/{action}"
        self._rest_client.post(url)

    def _send_action_v5(self, action: str, user_pin: str | None) -> None:
        url = f"scenes/{self.fibaro_id}/{action}"
        if user_pin:
            self._rest_client.post(url, {}, http_headers={"Fibaro-User-PIN": user_pin})
        else:
            self._rest_client.post(url, {})

    @staticmethod
    def read_scenes(rest_client: RestClient, api_version: int) -> list[SceneModel]:
        """Returns a list of scenes."""
        raw_data: list = rest_client.get("scenes")
        scenes: list[dict] = []
        for scene in raw_data:
            if "id" not in scene or "name" not in scene:
                _LOGGER.debug("Ignore scene because it does not contain id or name")
            else:
                scenes.append(scene)

        return [SceneModel(data, rest_client, api_version) for data in scenes]
