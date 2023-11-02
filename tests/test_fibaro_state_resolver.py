"""Test FibaroStateHandler class."""


from pyfibaro.fibaro_state_resolver import FibaroStateResolver

from .test_utils import load_fixture

refresh_payload = load_fixture("refresh.json")
refresh_extended_payload = load_fixture("refresh_extended.json")


def test_fibaro_state_resolver_event() -> None:
    """Test event resolver"""
    resolver = FibaroStateResolver(refresh_payload)
    events = resolver.get_events()
    assert events is not None
    assert len(events) == 2
    assert events[0].event_type == "DevicePropertyUpdatedEvent"
    assert events[0].fibaro_id == 28
    assert events[0].key_event_type == ""
    assert events[0].key_id == 0

    assert events[1].event_type == "PowerMetricsChangedEvent"
    assert events[1].fibaro_id is None
    assert events[1].key_event_type == ""
    assert events[1].key_id == 0


def test_fibaro_state_resolver_state_update() -> None:
    """Test event resolver"""
    resolver = FibaroStateResolver(refresh_payload)
    changes = resolver.get_state_updates()
    assert changes is not None
    assert len(changes) == 1
    assert changes[0].fibaro_id == 28
    assert changes[0].property_changes == {"value": "232.88"}


def test_fibaro_state_resolver_state_update_extended() -> None:
    """Test event resolver"""
    resolver = FibaroStateResolver(refresh_extended_payload)
    changes = resolver.get_state_updates()
    assert changes is not None
    assert len(changes) == 1
    assert changes[0].fibaro_id == 28
    assert changes[0].property_changes == {"value": "232.88"}
