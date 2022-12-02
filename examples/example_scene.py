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

    scenes = client.read_scenes()
    for scene in scenes:
        print(f"Scene {scene.fibaro_id}: {scene.name}")

        if scene.fibaro_id == 19:
            scene.start()
            scene.stop()


if __name__ == "__main__":
    main()
