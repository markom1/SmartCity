import json
import requests

response = requests.get("https://api.thingspeak.com/channels/621185/feeds.json?results")
todos = json.loads(response.text)
