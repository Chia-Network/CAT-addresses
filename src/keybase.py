import os
import requests


webhook_url = os.getenv("KEYBASE_WEBHOOK_URL", "http://localhost")


def keybase_alert(message: str):
    requests.post(webhook_url, headers={'Content-Type': 'text/text; charset=utf-8'}, data=message.encode('utf-8'))
