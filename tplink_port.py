#!/usr/bin/env python3

"""
    TPLink smart switch uses server-side authentication, so logging in on the browser leaves you logged in for
    any other applications running at the same IP address (I think).
    A form is submitted on the /login.cgi page with the username and password.
    The server doesn't respond with any cookie but then just associates your IP with the logged on IP.
    This is obviously completely insecure, but perhaps OK for a home network.  If you access the switch
    port from behind a firewall, it may be that you get access from more than one machine.

    Tested only with TL-SG1016PE

    To use create a credentials file in json format:
    $ cat ~/.tplink_config
    {
        "host": "192.168.0.101","
        "password": "mypassword"
    }
"""

import sys
import json
import httpx
import re
from pathlib import Path
from argparse import ArgumentParser
from functools import lru_cache
from bs4 import BeautifulSoup
from dataclasses import dataclass

HOME = Path.home()
DOT_FILE = HOME / ".tplink_config"


@lru_cache
def get_config():
    if not DOT_FILE.exists():
        sys.exit(f"Config file {DOT_FILE} not found")

    config = json.load(DOT_FILE.open())

    return {
        "login_form": {
            "username": "admin",  # Your username
            "password": config["password"],  # Your password
            "cpassword": "",  # Confirmation password, if needed
            "logon": "Login"  # Submit button value
        },
        "host": config["host"]
    }


def do_login(client):
    config = get_config()

    # Send a POST request to the login URL with the form data
    url = f"http://{config['host']}/logon.cgi"
    data = config["login_form"]
    response = client.post(url, data=data)

    # Check if the login request was successful
    if response.status_code != 200:
        sys.exit(f"Login failed with status code: {response.status_code}")


@dataclass
class PortValue:
    """Just one value for now, maybe expand later?"""
    state: int


def get_port_status(client):
    config = get_config()
    # Define the URL and form parameters
    response = client.get(f"http://{config['host']}/PortSettingRpm.htm")
    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find_all("script")[0]
    rex = re.compile(r"var all_info = {(.*?)}", re.M | re.DOTALL)
    match = rex.search(script.text)
    out = {}
    if match is not None:
        js = match.group(1)
        for line in js.split():
            field = line.strip()
            if ":" not in field:
                continue
            name, value = field.split(":")
            offs = value.rfind("]")
            if offs == -1:
                continue
            value_array = eval(value[:offs+1])
            out[name] = value_array

    port_values = []
    for port_num in range(0, 16):
        state = out["state"][port_num]
        port_value = PortValue(state=state)
        port_values.append(port_value)

    return port_values

        
def set_port(client, port_num, enabled):
    config = get_config()

    params = {
        "portid": port_num,
        "state": 1 if enabled else 0,
        "speed": 1,
        "flowcontrol": 0,
        "apply": "Apply"
    }

    response = client.get(f"http://{config['host']}/port_setting.cgi", params=params)
    print("Status Code:", response.status_code)


def main():
    parser = ArgumentParser(description="Enable port on TP-Link switch")
    parser.add_argument("port", nargs="?", type=int, help="Port number", choices=list(range(1, 16)))
    parser.add_argument("operation", nargs="?", type=str, help="Operation to perform", choices=["enable", "disable"])
    args = parser.parse_args()

    # Start an HTTP session
    with httpx.Client() as client:
        do_login(client)
        if args.operation is None:
            values = get_port_status(client)
            if args.port is None:
                for i, value in enumerate(values):
                    print(f"Port {i+1}: {'enabled' if value.state == 1 else 'disabled'}")
            else:
                value = values[args.port - 1]
                print(f"{'enabled' if value.state == 1 else 'disabled'}")
        else:
            set_port(client, args.port, args.operation == "enable")


if __name__ == "__main__":
    main()
