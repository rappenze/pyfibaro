"""Endpoint object to access the endpoint settings/info"""

from __future__ import annotations

from .common.rest_client import RestClient


class RoomModel:
    """Model of a room."""

    def __init__(self, data: dict) -> None:
        """One room."""
        self.raw_data = data

    @property
    def fibaro_id(self) -> int:
        """Room id"""
        return self.raw_data.get("id")

    @property
    def name(self) -> str:
        """Room name"""
        return self.raw_data.get("name")

    @staticmethod
    def read_rooms(rest_client: RestClient) -> list[RoomModel]:
        """Returns a list of rooms."""
        raw_data: list = rest_client.get("rooms")
        return [RoomModel(data) for data in raw_data]
