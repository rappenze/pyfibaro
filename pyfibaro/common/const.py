"""Constants for the fibaro client."""

# Timeout in seconds for http requests
TIMEOUT = 10

# Constant http headers sent with each request
HTTP_HEADERS = {
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "pyfibaro",
}

# Match serial number prefix to a interface version
API_VERSION_MATCHER = {"HC2": 4, "HCL": 4, "HC3": 5, "HC3L": 5, "YH": 5}

# Devices which are ignored
# iOS_device includes iOS and Android devices
IGNORE_DEVICE = ["HC_user", "VOIP_user", "iOS_device"]
