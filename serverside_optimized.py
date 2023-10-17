# Diese Datei auf dem Rasperyy Pi, die an der Maschine angeschlossen ist, ausführen! (STEP 1)
# Dieser Script empfängt die seriellen Daten 
# und verarbeitet diese automatisiert in der Datenbank database.db
# Diverse Variablen regeln verschiedene Funktionen, bitte 
# dementsprechend die Variablen setzen 


# Für das Testen mit simplen und vorgesetzten Variablen
# ZUM DEBUGGEN BESTIMMT!
test=True

# Alle Meldungen außer diese mit Status 1 werden ignoriert
statuseinsprio = True

# HAUPTPROGRAMM
import sqlite3
import serial
from datetime import datetime

s = serial.Serial()

con = sqlite3.connect("database.db")
cur = con.cursor()


# Prüfen, ob Datenbank existiert und falls nötig, erstellen
def checkDatabase():
    print("Datenbank wird geprüft")
    cur.execute('''CREATE TABLE IF NOT EXISTS data (
        datum_uhrzeit TIMESTAMP,
        status REAL,
        typnummer REAL,
        taktzeit REAL,
        tageszaehler REAL,
        endloszaehler REAL,
        platzhalter1 REAL,
        platzhalter2 REAL,
        platzhalter3 REAL
    )''')
    print("Datenbankprüfung abgeschlossen")
    
# Seriellen Port einrichten
def init_serial():
    print("Serieller Port wird eingerichtet")
    s.port = '/dev/ttyUSB0'
    s.baudrate = 9600
    s.bytesize = 8
    s.stopbits = serial.STOPBITS_ONE
    s.parity = serial.PARITY_NONE
    s.rts = True
    s.dtr = True
    s.timeout = None
    print("Serielle Eigenschaften: ")
    print(s.timeout)
    print(s.parity)

# In dieser Funktion öffnen wir den seriellen Port. 
# Wir schicken die nötigen Daten an den Port und warten auf die Rückmeldung.
# Die Funktion hat einen fail-safe, indem er nichts macht und wartet, bis 
# etwas zurückkommt.  
def serialueberwachung():
    if(s.isOpen()):
        xy = ("SET\n\r").encode('utf-8')
        s.write(xy)
        s.write("123\n\r").encode('utf_8')
        while(1):
            test = []
            serial_line = s.readline().decode("utf-8").strip()
            print(serial_line)
            if(serial_line is not None):
                # Hier wird geprüft, ob die empfangene Daten mit dem Status 1 gesendet wurde
                if(statuseinsprio == True):
                    # Nur Meldungen mit Status 1 dürfen wir es verarbeiten
                    if(serial_line.startswith('1.0')):
                        test.append(serial_line)
                        file = open("CAB690.txt", "w")
                        file.write(str(test))
                        file.close()

                        # Daten in ein Tuple umwandeln, um diese besser verarbeiten zu können
                        data_list = [float(value) for value in serial_line.split()]
                        data_tuple = tuple(data_list)

                        datenbankschreiben(data_tuple)


                # Es wird jede Meldung beachtet (diesen Teil ändern, falls man bei Status 5 etwas
                # etwas anderes machen soll)
                else:
                    test.append(serial_line)
                    file = open("CAB690.txt", "w")
                    file.write(str(test))
                    file.close()

                    # Daten in ein Tuple umwandeln, um diese besser verarbeiten zu können
                    data_list = [float(value) for value in serial_line.split()]
                    data_tuple = tuple(data_list)

                    datenbankschreiben(data_tuple)
    else:
        print("ERROR: Cannot open serial port!")
        return
                
    
# Diese Funktion dient nur zu Testzwecken.
# Hier werden gesendete Daten simuliert und wie in serialueberwachung() verarbeitet

def testueberwachung():
    testtuple = [
    (1.00, 1.00, 49.67, 45.00, 3879.00, 0.00, 0.00, 0.00)]
    for tuple in testtuple:
        if(statuseinsprio == True):
            # Nur Meldungen mit Status 1 dürfen wir es verarbeiten
            
            if(tuple[0]==1.0):
                datenbankschreiben(testtuple)
            else:
                print("Meldung wird ignoriert, da nicht prio ist!")
        else:
                datenbankschreiben(testtuple)
    

def datenbankschreiben(data_tuple):
    # Datum und Uhrzeit in die Datenbank im Nachhinein einfügen
    jetzt = datetime.now()
    datum_uhrzeit = jetzt.strftime('%d.%m.%Y %H:%M:%S')
    for item in data_tuple:
        cur.execute("INSERT INTO data (datum_uhrzeit, status, typnummer, taktzeit, tageszaehler, endloszaehler, platzhalter1, platzhalter2, platzhalter3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (datum_uhrzeit, *item))
    # Daten speichern
    con.commit()
    
    # Daten zum anzeigen auswählen
    cur.execute("SELECT * FROM data")
    # Anzeigen
    print("Datum und Uhrzeit\tStatus\tTypnummer\tTaktzeit\tTageszähler\tEndloszähler")
    print("-" * 80)
    for row in cur.fetchall():
        print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}")
    # Datenbank schließen
    con.close()

    


# Hauptfunktion
def main():
    checkDatabase()
    init_serial()
    if(test):
        testueberwachung()
    else:
        serialueberwachung()


if __name__ =="__main__":
    main()
