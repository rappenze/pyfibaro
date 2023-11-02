"""State object resolver for fibaro home center."""
from __future__ import annotations

import logging

from typing import Any

_LOGGER = logging.getLogger(__name__)


class FibaroEvent:
    """A fibaro event returned by state handler."""

    def __init__(self, data: dict) -> None:
        """Constructor to init the object with the raw data."""
        self.raw_data = data

    @property
    def event_type(self) -> str:
        """Returns the event type as string.

        Most known event is "CentralSceneEvent" which is used for button press events.
        """
        return self.raw_data.get("type", "")

    @property
    def fibaro_id(self) -> int | None:
        """The device id which throws the event. Not all events are related to a device."""
        data = self.event_data
        # id is used by HC3, deviceId by HC2
        fibaro_id = data.get("id", data.get("deviceId"))
        if fibaro_id is None:
            return None
        return int(fibaro_id)

    @property
    def event_data(self) -> dict:
        """Returns the event data in raw format."""
        return self.raw_data.get("data", {})

    @property
    def key_id(self) -> int:
        """Returns the key id."""
        return int(self.event_data.get("keyId", 0))

    @property
    def key_event_type(self) -> str:
        """Returns the key event attribute.

        For example Pressed, Released, HeldDown, ...
        """
        return self.event_data.get("keyAttribute", "")


class FibaroStateChange:
    """A fibaro state change returned by state handler."""

    def __init__(self, data: dict) -> None:
        """Constructor to init the object with the raw data."""
        self.raw_data = data

    @property
    def fibaro_id(self) -> int:
        """The device id which throws the event."""
        return int(self.raw_data.get("id"))

    @property
    def property_changes(self) -> dict[str, Any]:
        """The changes in the device properties."""
        result: dict[str, Any] = {}

        for property_name, value in self.raw_data.items():
            # Ignore some attributes which are not relevant or returned separately
            if property_name in ("log", "logTemp", "id"):
                continue
            result[property_name] = value

        return result


class FibaroStateResolver:
    """State resolver allows typed access to a state object retunred by fibaro home center."""

    def __init__(self, data: dict) -> None:
        """Init the object with the raw event object."""
        self.raw_data = data

    def get_events(self) -> list[FibaroEvent]:
        """Extract events from the state handle object."""
        return [FibaroEvent(data) for data in self.raw_data.get("events", [])]

    def get_state_updates(self) -> list[FibaroStateChange]:
        """Extract state changes from the state handle object."""
        return [FibaroStateChange(data) for data in self.raw_data.get("changes", [])]
