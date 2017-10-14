import schedule
import time
import json
import requests

api_url = "https://onesignal.com/api/v1/notifications"
header = {"Content-Type": "application/json; charset=utf-8",
          "Authorization": "Basic MzgyODMyZjQtMmE4Ni00NzkzLWEwMDEtMDk4YmY2ZjY2ZmEy"}

payload = {
    "app_id": "3225cee9-5d6f-4e40-8f7e-328a3aa61e4d",
    "included_segments": ["All"],
    "contents": {"en": "English Message"},
    "headings": {'en': "asdsadsada! ;>"},
    "data": {"all": "info", "goes": "here", '.': True},
}


def send_notification():
    req = requests.post(api_url, headers=header, data=json.dumps(payload))
    print(req.status_code, req.reason)

schedule.every().second.do(send_notification)

while True:
    schedule.run_pending()
    time.sleep(1)
