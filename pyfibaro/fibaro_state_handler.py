"""State handler for fibaro home center."""

import logging
import threading

from .common.const import REFRESH_STATE_TIMEOUT
from .common.rest_client import RestClient

_LOGGER = logging.getLogger(__name__)


class FibaroStateHandler(threading.Thread):
    """State handler which uses the refreshStates
    endpoint to pull state changes from home center.
    """

    def __init__(self, rest_client: RestClient, callback: callable) -> None:
        """Create the state handler and start the background thread."""

        super().__init__(name=f"Thread {__name__}")

        self._rest_client = rest_client
        self._callback = callback
        self._stop_flag = threading.Event()

        # stop unconditionally on exit
        self.daemon = True

        self.start()

    def run(self) -> None:
        """State Handler main loop which runs in this thread."""

        _LOGGER.info("Starting the state change handler")
        last = 0

        while not self._is_stopped_flag():
            sleep_time = 1
            attempt = 1
            success = False

            while not success and not self._is_stopped_flag():
                try:
                    state = self._rest_client.get(
                        f"refreshStates?last={last}", timeout=REFRESH_STATE_TIMEOUT
                    )
                    _LOGGER.debug(state)

                    last = state.get("last")
                    success = True
                except Exception as ex:
                    _LOGGER.warning("Connection Error (%s). Error: %s", attempt, ex)
                    attempt += 1

                    if attempt == 3:
                        sleep_time = 30
                        _LOGGER.info("Fallback to 30-second connection retry timer.")

                    self._stop_flag.wait(sleep_time)

                if success:
                    try:
                        self._callback(state)
                    except Exception as ex:
                        _LOGGER.warning("Error in state change callback: %s", ex)


        _LOGGER.info("State change handler stopped.")

    def _is_stopped_flag(self) -> bool:
        return self._stop_flag.is_set()

    def stop(self) -> None:
        """Stop the state handler."""
        _LOGGER.debug("Stopping the state change handler")

        # no effect on pending request
        self._rest_client.close()
        self._stop_flag.set()
