"""Code for checking for neutering appointments at https://phs-spca.org/."""

import requests
import logging
import time
import os
from typing import Iterable

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PO_TOKEN = os.environ.get("PO_TOKEN")
PO_USER = os.environ.get("PO_USER")


class PushOver:
    BASE_URL = "https://api.pushover.net"
    """Client class for PushOver API"""

    def __init__(self, token: str, user: str):
        self.token = token
        self.user = user
        self.session = requests.Session()

    def send(self, msg: str) -> bool:
        url = self.BASE_URL + "/1/messages.json"
        data = {"token": self.token, "user": self.user, "message": msg}
        resp = self.session.post(url, data=data)
        if resp.ok:
            logger.info(f"successfully sent message: {msg}")
        else:
            logger.error(f"failed to send message: {msg}")
            return False
        return True


def send_test_message():
    pushover_test_client = PushOver(token=PO_TOKEN, user=PO_USER)
    pushover_test_client.send("Test message from Pushover")


def get_spca() -> Iterable[str]:
    url = "https://clinichq.com/online/eedeab6f-5fee-495a-b3aa-6daeb032be72/dates"
    data = {
        "specieId": 2,
        "genderId": 1,
        "weight": 5,
    }
    resp = requests.post(url, json=data)
    if resp.ok:
        return resp.json()
    logging.error(f"request failed with error: {resp.text}")
    return list()


def main():
    print("script started")
    send_test_message()

    pushover_client = None
    logging.info("Starting tracking for spca")
    if PO_TOKEN and PO_USER:
        pushover_client = PushOver(token=PO_TOKEN, user=PO_USER)
        pushover_client.send("Starting tracking for spca")
        print(PushOver)
        print(pushover_client.user)
        print(pushover_client.token)
    while True:
        try:
            if dates := get_spca():
                logging.info(f"found dates: {dates}")
                if pushover_client:
                    pushover_client.send(f"Found dates: {dates}\nhttps://clinichq.com/online/eedeab6f-5fee-495a-b3aa"
                                         f"-6daeb032be72")
        except Exception:
            pass
        time.sleep(60)


if __name__ == "__main__":
    main()
