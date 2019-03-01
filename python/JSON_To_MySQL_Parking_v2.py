import mysql.connector, urllib.request, json, threading, time

"""
    String za spajanje na MySQL bazu podataka.
"""
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


"""
    Povlacenje JSON-a sa ThingSpeak servera.
    urllib.request.urlopen salje http request stranici, i zatim json.loads pretvara json u python objekte.
"""

cursor = conn.cursor()
with urllib.request.urlopen("https://api.thingspeak.com/channels/629316/feeds.json?api_key=Y4KQ33L0LZM0GSZX") as url:
    data = json.loads(url.read().decode())
with urllib.request.urlopen("https://api.thingspeak.com/channels/629316.json?api_key=Y4KQ33L0LZM0GSZX") as url:
    channelData = json.loads(url.read().decode())

#json_string = json.dumps(data, indent=2)
#print(json_string)


"""
    Ispred metode Entry su definirane liste za inicijalni unos podataka.
    Metoda Entry izvrsava inicijalni unos podataka u bazu.
    for u pythonu funkcionira kao foreach u C# sto znaci:
    npr. Svaki entry_id koji se nalazi u dijelu json-a pod ['feeds'] se stavlja u listu listEntryID .
"""

listEntryID = []
listParkirnoMjesto1 = []
listParkirnoMjesto2 = []
listParkirnoMjesto3 = []

def Entry():
    for entryID in data['feeds']:
        listEntryID.append(entryID['entry_id'])

    for ParkirnoMjesto1 in data['feeds']:
        listParkirnoMjesto1.append(ParkirnoMjesto1['field1'])

    for ParkirnoMjesto2 in data['feeds']:
        listParkirnoMjesto2.append(ParkirnoMjesto2['field2'])

    for ParkirnoMjesto3 in data['feeds']:
        listParkirnoMjesto3.append(ParkirnoMjesto3['field3'])

    for i in range(0, 99):
        insert = "INSERT INTO parkingPodac(entry_id, ParkirnoMjesto1, ParkirnoMjesto2, ParkirnoMjesto3) VALUES(%s, %s, %s, %s)"
        cursor.execute(insert, (listEntryID[i], listParkirnoMjesto1[i], listParkirnoMjesto2[i], listParkirnoMjesto3[i]))

    print("Podaci upisani u bazu podataka.")
    conn.commit()
    
Entry()

"""
    Ispred metode updateDatabase definirane su liste za azuriranje baze podataka.
    !!! updateDatabase() je pozvan tek u while loopu na kraju koda !!!
    Metoda updateDatabase() azurira bazu podataka:
    1. Posalje se novi request za json sa thingspeak-a, ali ovaj put samo za zadnjim unesenim podatkom (zato je &results=1 u URL-u)
    2. Podaci se stavljaju u updated liste i zatim na isti nacin kao i kod Entry() metode upisuju u bazu podataka
    3. Nakon toga se liste ociste i ostanu prazne tako da su spremne za novi update. To se radi naredbom npr. del updateEntryID[:]
    4. Postavlja se updatedLastEntryID na najnoviji last_entry_id. To je polje u jsonu koje nam govori koje je id od zadnjeg upisanog podatka.
"""

updateEntryID = []
updateParkirnoMjesto1 = []
updateParkirnoMjesto2 = []
updateParkirnoMjesto3 = []

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
        update = "INSERT INTO parkingPodac(entry_id, ParkirnoMjesto1, ParkirnoMjesto2, ParkirnoMjesto3) VALUES (%s, %s, %s, %s)"
        cursor.execute(update, (updateEntryID[i], updateParkirnoMjesto1[i], updateParkirnoMjesto2[i], updateParkirnoMjesto3[i]))
    conn.commit()
    
    del updateEntryID[:]
    del updateParkirnoMjesto1[:]
    del updateParkirnoMjesto2[:]
    del updateParkirnoMjesto3[:]

    updatedLastEntryID = channelData['last_entry_id']


"""
    while True loop preko metoda checkForUpdate() stalno provjerava je li se promjenio 'last_entry_id' tako da:
    1. Stalno se provjerava 'last_entry_id' naredbom:
            lastEntryID = channelData['last_entry_id']
    2. U if petlji se usporeduje sa updatedLastEntryID koji je IZVAN while petlje i metode postavljen na isto:
            updatedLastEntryID = channelData['last_entry_id']

    Ako su obije varijable iste, baza podataka se ne mijenja i ispisuje se poruka da je azurirana.
    U suprotnom, baza se azurira i zatim se poziva metoda updateDatabase() koja na svom kraju
    postavlja novi updatedLastEntryID.

    time.sleep naredba vrti while loop svakih 5 sekundi.
"""

delay = 5

updatedLastEntryID = channelData['last_entry_id']

while True:
    lastEntryID = channelData['last_entry_id']
    print("lastEntryID = " + str(lastEntryID))
    print("updatedLastEntryID = " + str(updatedLastEntryID))
    def checkForUpdate():
        if (lastEntryID == updatedLastEntryID):
            print("Baza je azurirana.")
        else:
            print("Azuriranje baze podataka...")
            updateDatabase()
            print("Baza podataka azurirana.")
    checkForUpdate()
    time.sleep(delay)

conn.close()
