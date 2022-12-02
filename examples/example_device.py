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
    client.connect()

    devices = client.read_devices()
    for device in devices:
        print(f"Device {device.fibaro_id}: {device.name}")
        if device.fibaro_id == 72:
            device.execute_action("turnOn")

        if device.fibaro_id == 347:
            device.execute_action("setValue", [99])


if __name__ == "__main__":
    main()
