"""Manual test class."""

import logging

from pyfibaro.fibaro_client import FibaroClient

from . import FIBARO_PASSWORD, FIBARO_URL, FIBARO_USERNAME


def main():
    """Main method for testing purposes"""

    logging.basicConfig(level=logging.DEBUG)

    print("Start test...")

    client = FibaroClient(FIBARO_URL)
    client.set_authentication(FIBARO_USERNAME, FIBARO_PASSWORD)

    rooms = client.read_rooms()
    for room in rooms:
        print(f"Room {room.fibaro_id}: {room.name}")


if __name__ == "__main__":
    main()
