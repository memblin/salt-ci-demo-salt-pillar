#!/usr/bin/env python3

import json
import logging
import os
import requests

from collections import defaultdict


# Logging
logging.basicConfig(format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Import Salt API Config Environment Variables
API_BASE_URL = os.getenv('API_BASEURL', "https://salt-ci02.local:8000")
API_CA_CERT_PATH = os.getenv('API_CA_CERT_PATH', "/etc/pki/ca-trust/source/anchors/internal-ca.crt")
API_USERNAME = os.getenv('API_USERNAME', "salt-ci-user")
API_PASSWORD = os.getenv('API_PASSWORD', "salt-ci-password")

# Import GitHub Environment Variables
TARGET_PILLARENV = os.getenv('TARGET_PILLARENV', 'base')
INCOMING_PILLARENV = os.getenv('INCOMING_PILLARENV', 'dev.change_web_pillar')
MINION_IDS = os.getenv('MINION_IDS', '["web01.local", "srv01.local" ,"salt.local", "salt-ci01.local"]')


def consolidate_data(data):
    server_data = defaultdict(lambda: defaultdict(list))
    for item in data:
        parts = item.split(':')
        server_id = parts[0]
        path_string = ':'.join(parts[1:])
        change_type = path_string.split(';')[-1]
        path_string = path_string.rsplit(';', 1)[0]
        server_data[server_id][change_type].append(path_string)
    return server_data


def main():
    """
    Main function
    """
    # Create a session object
    session = requests.Session()
    session.verify = API_CA_CERT_PATH

    baseurl = API_BASE_URL
    username = API_USERNAME
    password = API_PASSWORD

    # Authenticate to the API
    login_response = session.post(
        baseurl + "/login",
        json={
            "username": username,
            "password": password,
            "eauth": "pam",
        },
        timeout=90,
    )

    if login_response.ok:
        log.debug("Logged in to salt-api successfully")

    salt_commands = [
        {
            "client": "runner",
            "fun": "citools.validate_pr",
            "arg": [MINION_IDS, TARGET_PILLARENV, INCOMING_PILLARENV],
        },
    ]

    if login_response.ok:
        # We authenticated successfully
        salt_api_response = session.post(
            baseurl + "/",
            json=salt_commands,
            timeout=90,
        )

        log.debug(f"Salt API Response JSON: {salt_api_response.json()}")

        data = salt_api_response.json()["return"][0]

        consolidated_api_data = consolidate_data(data)

        log.debug(f"Consolidated API Data: {consolidated_api_data}")

        # for minion, pillars in consolidated_api_data.items():
        #     log.info(f"Changes for Minion ID: {minion}")
        #     for change_type, pillar in pillars.items():
        #         log.info(f"Change Type: {change_type}")
        #         for pillar_path in pillar:
        #             log.info(f"Pillar Path: {pillar_path}")

        print(f"{json.dumps(consolidated_api_data, indent=4)}")

        # with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        #     fh.write(f"{json.dumps(consolidated_api_data, indent=4)}")

        # Logout the API Session
        logout_response = session.post(
            baseurl + "/logout",
            timeout=90,
        )

        if logout_response.ok:
            log.debug(f"Logged out of salt-api")

if __name__ == "__main__":
    main()
