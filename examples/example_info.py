"""Manual test class."""

import logging

from pyfibaro.fibaro_client import FibaroClient
import urllib3
from . import FIBARO_URL


def main():
    """Main method for testing purposes"""

    logging.basicConfig(level=logging.DEBUG)

    print("Start test...")

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    client = FibaroClient(FIBARO_URL)
    info = client.read_info()

    print(f"Serial no: {info.serial_number}")
    print(f"Version: {info.current_version}")
    print(f"HC Name: {info.hc_name}")
    print(f"API version: {info.api_version}")


if __name__ == "__main__":
    main()
