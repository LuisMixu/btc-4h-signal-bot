"""Temporary one-off diagnostic: attempts a real Telegram sendMessage using
the repo's actual secrets and prints Telegram's raw JSON response (including
the error description on failure). Never prints the token itself. Delete
this file and its workflow once the Telegram delivery issue is diagnosed."""
import json
import os
import urllib.request
import urllib.error

token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

print("TELEGRAM_BOT_TOKEN present:", bool(token), "length:", len(token) if token else 0)
print("TELEGRAM_CHAT_ID value:", repr(chat_id))

if not token or not chat_id:
    print("ERROR: one or both secrets are missing/empty in this repo.")
    raise SystemExit(1)

url = f"https://api.telegram.org/bot{token}/sendMessage"
data = json.dumps({"chat_id": chat_id, "text": "Diagnose-Test vom BTC 4h Signal Bot -- wenn du das siehst, funktioniert alles."}).encode()
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode()
        print("HTTP status:", resp.status)
        print("Response body:", body)
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print("HTTP error status:", e.code)
    print("Response body:", body)
except urllib.error.URLError as e:
    print("URLError:", e)
