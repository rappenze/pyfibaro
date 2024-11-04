"""Constants for the fibaro client."""

# Timeout in seconds for http requests
DEFAULT_TIMEOUT = 10

# HC 3 needs a big timeout for refresh states request,
# it waits up to 30 seconds before a response is sent
REFRESH_STATE_TIMEOUT = 35

# Constant http headers sent with each request
HTTP_HEADERS = {
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "pyfibaro",
}

# Match serial number prefix to a interface version
API_VERSION_MATCHER = {"HC2": 4, "HCL": 4, "HC3": 5, "HC3L": 5, "YH": 5, "ZB": 5}

# Devices which are ignored
# iOS_device includes iOS and Android devices
IGNORE_DEVICE = ["HC_user", "VOIP_user", "iOS_device"]
