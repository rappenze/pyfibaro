# pyfibaro

[![license](https://img.shields.io/pypi/l/pyatmo.svg)](https://github.com/rappenze/pyfibaro/blob/main/LICENSE)
[![pypi package](https://img.shields.io/pypi/v/pyfibaro)](https://pypi.org/project/pyfibaro/)
![python version](https://img.shields.io/pypi/pyversions/pyfibaro)

This project has no relation to the fibaro company.

Simple API to access fibaro home center from Python 3. For more detailed information see

[Home center 2 / Home center lite](https://manuals.fibaro.com/knowledge-base-browse/rest-api/)

[Home center 3 / Home center 3 lite / Yubii Home](https://www.fibaro.com/dev/)

The pyfibaro library was created for integrating the fibaro home center with home assistant but can be used also in other projects.

# Install

To install pyfibaro simply type

`pip install pyfibaro`

# Authentication

All endpoints of the fibaro home center except info and login status needs an authenticated user.
Just create a user in the fibaro home center with enough rights.

# Development

Easiest way to start developing is to use Visual Studio Code + devcontainer.

## Prerequisites

[Docker](https://docs.docker.com/get-docker/)

[Visual Studio code](https://code.visualstudio.com/)

## Getting started

1. Fork this repository
2. Enter the following link in your browser:
   `vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=<your github repository url>`
3. When Visual Studio Code asks if you want to install the Remote extension, click "Install".

For additional information about Visual Studio Code + devcontainer [learn more about devcontainers](https://code.visualstudio.com/docs/devcontainers/containers).

# Testing

Run the script

`script/test`

This will run all unit tests with code coverage enabled.

# Usage

```python
client = FibaroClient("http://192.168.1.2/api/")
client.set_authentication("your_fibaro_username", "your_fibaro_password")
client.connect()

devices = client.read_devices()
for device in devices:
    print(f"Device {device.fibaro_id}: {device.name}")

devices[10].execute_action("turnOn")
```

See folder `examples` for additional examples.
