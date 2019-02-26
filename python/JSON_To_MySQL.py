import mysql.connector, requests, urllib.request, json
from mysql.connector import Error
import datetime

try:
    conn = mysql.connector.connect(
    host='localhost',
    database='smartcity',
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

list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
list7 = []
list8 = []
list9 = []

for stanicaID in data['feeds']:
   list1.append(stanicaID['field1'])

for temperaturaZraka in data['feeds']:
    list2.append(temperaturaZraka['field2'])

for vlagaZraka in data['feeds']:
    list3.append(vlagaZraka['field3'])

for brzinaVjetra in data['feeds']:
    list4.append(brzinaVjetra['field4'])

for smjerVjetra in data['feeds']:
    list5.append(brzinaVjetra['field5'])

for kolicinaPadalina in data['feeds']:
    list6.append(kolicinaPadalina['field6'])

for tlakZraka in data['feeds']:
    list7.append(tlakZraka['field7'])

for entryid in data['feeds']:
    list8.append(entryid['entry_id'])

for createdat in data['feeds']:
    list9.append(entryid['created_at'])

for i in range(0,6):
    insert = "INSERT INTO meteoroloskastanica (entry_id, stanicaID, temperaturaZraka, vlagaZraka, brzinaVjetra, smjerVjetra, kolicinaPadalina, tlakZraka, created_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert, (list8[i], list1[i], list2[i], list3[i], list4[i], list5[i], list6[i], list7[i], list9[i]))

conn.commit()
conn.close()
