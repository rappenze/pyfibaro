"""Helpers for fibaro tests."""

import json
from typing import Any

TEST_BASE_URL = "http://192.168.1.166/api/"
TEST_USERNAME = "admin"
TEST_PASSWORD = "admin"


def load_fixture(filename: str) -> Any:
    """Load a json file."""
    with open(f"tests/fixture/{filename}", encoding="UTF-8") as file:
        return json.load(file)
