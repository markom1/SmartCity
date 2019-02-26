import mysql.connector, urllib.request, json, threading, time

try:
    conn = mysql.connector.connect(
    host='portmap.io',
    port='61974',
    database='parking',
    user='test',
    password='123');
    print("Povezivanje na bazu podataka uspjesno.")
except EnvironmentError as e:
    print("Povezivanje neuspjelo. Provjerite podatke")

databaseIsEmpty = True

cursor = conn.cursor()
with urllib.request.urlopen("https://api.thingspeak.com/channels/629316/feeds.json?api_key=Y4KQ33L0LZM0GSZX") as url:
    data = json.loads(url.read().decode())
with urllib.request.urlopen("https://api.thingspeak.com/channels/629316.json?api_key=Y4KQ33L0LZM0GSZX") as url:
    channelData = json.loads(url.read().decode())

# json_string = json.dumps(data, indent=2)
# print(json_string)

listEntryID = []
listParkirnoMjesto1 = []
listParkirnoMjesto2 = []
listParkirnoMjesto3 = []

def initialDataEntry():
    for entryID in data['feeds']:
        listEntryID.append(entryID['entry_id'])

    for ParkirnoMjesto1 in data['feeds']:
        listParkirnoMjesto1.append(ParkirnoMjesto1['field1'])

    for ParkirnoMjesto2 in data['feeds']:
        listParkirnoMjesto2.append(ParkirnoMjesto2['field2'])

    for ParkirnoMjesto3 in data['feeds']:
        listParkirnoMjesto3.append(ParkirnoMjesto3['field3'])

    #lastEntryID = channelData['last_entry_id']

    for i in range(0, 100):
        insert = "INSERT INTO parkingPodaci(entry_id, ParkirnoMjesto1, ParkirnoMjesto2, ParkirnoMjesto3) VALUES(%s, %s, %s, %s)"
        cursor.execute(insert, (listEntryID[i], listParkirnoMjesto1[i], listParkirnoMjesto2[i], listParkirnoMjesto3[i]))

lastEntryID = channelData['last_entry_id']

updateEntryID = []
updateParkirnoMjesto1 = []
updateParkirnoMjesto2 = []
updateParkirnoMjesto3 = []
updateLastEntryID = []

def updateDatabase():
    with urllib.request.urlopen("https://api.thingspeak.com/channels/629316/feeds.json?api_key=Y4KQ33L0LZM0GSZX&results=1") as url:
        updateData = json.loads(url.read().decode())

    for newEntryID in updateData['feeds']:
        updateEntryID.append(newEntryID['entry_id'])

    for newParkirnoMjesto1 in updateData['feeds']:
        updateParkirnoMjesto1.append(newParkirnoMjesto1['field1'])

    for newParkirnoMjesto2 in updateData['feeds']:
        updateParkirnoMjesto2.append(newParkirnoMjesto2['field2'])

    for newParkirnoMjesto3 in updateData['feeds']:
        updateParkirnoMjesto3.append(newParkirnoMjesto3['field3'])

    for i in range(0,1):
        update = "INSERT INTO parkingPodaci(entry_id, ParkirnoMjesto1, ParkinroMjesto2, ParkirnoMjesto3) VALUES (%s, %s, %s, %s)"
        cursor.execute(update, (updateEntryID[i], updateParkirnoMjesto1[i], updateParkirnoMjesto2[i], updateParkirnoMjesto3[i]))

    del updateEntryID[:]
    del updateParkirnoMjesto1[:]
    del updateParkirnoMjesto2[:]
    del updateParkirnoMjesto3[:]

    lastEntryID = channelData['last_entry_id']

    checkForUpdate()

def checkForUpdate():
    databaseIsEmpty = False
    lastEntryUpdated = channelData['last_entry_id']
    if lastEntryUpdated == lastEntryID:
        print("Baza je azurirana.")
        lastEntryUpdated = 0
    else:
        print("Azuriranje baze...")
        updateDatabase()

if databaseIsEmpty == True:
    print("Tablica je prazna. Dodavanje postojećih podataka...")
    initialDataEntry()
    checkForUpdate()
else:
    databaseIsEmpty == False
    checkForUpdate()

conn.commit()
conn.close()
