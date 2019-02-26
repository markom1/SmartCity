import mysql.connector, requests, urllib.request, json
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
    host='localhost',
    database='meteoroloskaStanica',
    user='root',
    password='superpassword');

    print("Povezivanje na bazu podataka uspjesno.")

except Error as e:
    print(e)

cursor = conn.cursor()
with urllib.request.urlopen("https://api.thingspeak.com/channels/630034/feeds.json?api_key=Y4KQ33L0LZM0GSZX") as url:
    data = json.loads(url.read().decode())

json_string = json.dumps(data, indent=2)
print(json_string)
    
if 
