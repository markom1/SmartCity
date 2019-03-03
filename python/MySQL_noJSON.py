import mysql.connector, time, sys

try:
    conn = mysql.connector.connect(
    host='portmap.io',
    port='61974',
    database='testiranje',
    user='test',
    password='123');
    print("Povezivanje na bazu podataka uspjesno.")
except EnvironmentError as e:
    print("Povezivanje neuspjelo. Provjerite podatke")

cursor = conn.cursor()

def query():
    cursor.execute("SELECT * FROM test")
    podaci = cursor.fetchall()
    
    print("\nSvi podaci u bazi test: ")
    for row in podaci:
        print(row)
        

def provjera():
    odgovor = input("Zelite li jos nesto unijeti? d/n ")
    if (odgovor == "d"):
        insert()
    elif (odgovor == "n"):
        query()
        #sys.exit("/nProgram zavrsen.")

def insert():
    unos = input("Unesite sto zelite dodati u bazu: ")
    insert = "INSERT INTO test(unos) VALUES(%s)"
    cursor.execute(insert, (unos,))
    conn.commit()
    provjera()

insert()
provjera()

conn.commit()
conn.close()
