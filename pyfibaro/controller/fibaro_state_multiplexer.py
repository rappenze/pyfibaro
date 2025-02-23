"""Fibaro state multiplexer receives all information from the push channel and
provides methods to register listeners for specific devices.
"""

from typing import Any
from collections.abc import Callable

from pyfibaro.fibaro_client import FibaroClient
from pyfibaro.fibaro_state_resolver import FibaroEvent, FibaroStateChange, FibaroStateResolver


class FibaroStateMultiplexer:
    """State and event multiplexer."""

    def __init__(self, fibaro_client: FibaroClient) -> None:
        """Construct the fibaro manager."""
        self._fibaro_client = fibaro_client

        self._change_listeners: dict[
            int, list[Callable[[FibaroStateChange], None]]
        ] = {}
        self._event_listeners: dict[int,
                                    list[Callable[[FibaroEvent], None]]] = {}

    def start(self) -> None:
        """Connect push channel and start change and event dispatching."""
        self._fibaro_client.register_update_handler(self._on_change)

    def stop(self) -> None:
        """Disconnect push channel so that no change and events are dispatched anymore."""
        self._fibaro_client.unregister_update_handler()

    def add_change_listener(
        self, fibaro_id: int, listener: Callable[[FibaroStateChange], None]
    ) -> Callable[[], None]:
        """Add a listener to get property changes."""
        change_listeners = self._change_listeners.setdefault(fibaro_id, [])
        change_listeners.append(listener)

        return lambda: change_listeners.remove(listener)

    def add_event_listener(
        self, fibaro_id: int, listener: Callable[[FibaroEvent], None]
    ) -> Callable[[], None]:
        """Add central scene event listener."""
        event_listeners = self._event_listeners.setdefault(fibaro_id, [])
        event_listeners.append(listener)

        return lambda: event_listeners.remove(listener)

    def _on_change(self, state: Any) -> None:
        resolver = FibaroStateResolver(state)

        for state_change in resolver.get_state_updates():
            fibaro_id = state_change.fibaro_id
            for listener in self._change_listeners.get(fibaro_id, []):
                listener(state_change)

        for event in resolver.get_events():
            # event does not always have a fibaro id, therefore it is
            # essential that we first check for it
            fibaro_id = event.fibaro_id
            if fibaro_id:
                for listener in self._event_listeners.get(fibaro_id, []):
                    listener(event)
