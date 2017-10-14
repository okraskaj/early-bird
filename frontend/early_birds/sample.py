import json

import requests

header = {"Content-Type": "application/json; charset=utf-8",
          "Authorization": "Basic MzgyODMyZjQtMmE4Ni00NzkzLWEwMDEtMDk4YmY2ZjY2ZmEy"}

payload = {
      "app_id": "3225cee9-5d6f-4e40-8f7e-328a3aa61e4d",
       "included_segments": ["All"],
       "contents": {"en": "English Message"},
       "headings": {'en': "asdsadsada! ;>"},
       "data": {"all": "info", "goes": "here", '.': True},
      }

req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

print(req.status_code, req.reason)
