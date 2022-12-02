"""Manual test class."""

import logging
import time

from pyfibaro.fibaro_client import FibaroClient

from . import FIBARO_PASSWORD, FIBARO_URL, FIBARO_USERNAME


def state_callback(event) -> None:
    """Report state updates to the console."""
    print(f"State updates: {event}")


def main():
    """Main method for testing purposes"""

    logging.basicConfig(level=logging.DEBUG)

    print("Start test...")

    client = FibaroClient(FIBARO_URL)
    client.set_authentication(FIBARO_USERNAME, FIBARO_PASSWORD)
    client.connect()

    client.register_update_handler(state_callback)

    time.sleep(60)


if __name__ == "__main__":
    main()
