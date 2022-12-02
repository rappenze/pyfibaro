"""Manual test class."""

import logging

from pyfibaro.fibaro_client import FibaroClient

from . import FIBARO_PASSWORD, FIBARO_URL, FIBARO_USERNAME


def main():
    """Main method for testing purposes"""

    logging.basicConfig(level=logging.DEBUG)

    print("Start test...")

    client = FibaroClient(FIBARO_URL)
    logged_in = client.connect()

    client.set_authentication(FIBARO_USERNAME, FIBARO_PASSWORD)

    logged_in = client.connect()
    print(f"Logged in: {logged_in}")


if __name__ == "__main__":
    main()
