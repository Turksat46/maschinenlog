# Einfache Testdatei
# Importieren wichtiger Bibliotheken
import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

# Befehl, um eine Datenbank zu erstellen, wenn diese noch nicht vorhanden ist
cur.execute('''CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY,
        status REAL,
        typnummer REAL,
        taktzeit REAL,
        tageszaehler REAL,
        endloszaehler REAL,
        platzhalter1 REAL,
        platzhalter2 REAL,
        platzhalter3 REAL,
        platzhalter4 REAL
)''')
print('Database initialized!')

# Provisorische Testdaten
testdaten = [
    (1, 1.00, 1.00, 49.67, 45.00, 3879.00, 0.00, 0.00, 0.00),
    (2, 1.00, 2.00, 58.45, 50.00, 6628.00, 0.00, 0.00, 0.00)
]

# Die Daten in die Datenbank senden
for item in testdaten:
    cur.execute("INSERT INTO data (status, typnummer, taktzeit, tageszaehler, endloszaehler, platzhalter1, platzhalter2, platzhalter3, platzhalter4) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", item)

# Daten zum anzeigen auswählen
cur.execute("SELECT * FROM data")

# Anzeigen lassen
print("ID\tStatus\tTypnummer\tTaktzeit\tTageszähler\tEndloszähler")
print("-" * 80)
for row in cur.fetchall():
    print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}")

# Verbindung zur Datenbank schließen
con.commit()
con.close()