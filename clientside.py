# Diese Datei auf dem zweiten Rasperry Pi ausführen (Step 2)
# Diese Datei beinhaltet die GUI.
# Besondere Funktionen:
# aktualisieren (aktualisiert die aktuelle Meldungen Liste und Durschnittstaktzeit)

import sqlite3
import tkinter as tk
from tkinter import ttk

con = sqlite3.connect("database.db")
cur = con.cursor()

root = tk.Tk()
root.title("Daten")

# Header
frame1 = ttk.LabelFrame(root, padding=(5, 5))
frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

# Wahrscheinlich Modellnummer
label = tk.Label(frame1, text="R69_CSH5")
label.pack()

# Taktzeit
frame2 = ttk.LabelFrame(root,text="∅ Taktzeit", padding=(10,10))
frame2.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
label2 = tk.Label(frame2, text="...")
label2.pack()

# Schicht 1
frame3 = ttk.LabelFrame(root,text="Schicht 1" , padding=(10,10))
frame3.grid(row=1, column=1, padx=10, pady=10, sticky="nw")
label3 = tk.Label(frame3, text="178")
label3.pack()

# Schicht 2
frame4 = ttk.LabelFrame(root, text="Schicht 2", padding=(10,10))
frame4.grid(row=1, column=2, padx=10, pady=10, sticky="nw")
label4 = tk.Label(frame4, text="195")
label4.pack()

# Schicht 3
frame5 = ttk.LabelFrame(root, text="Schicht 3", padding=(10,10))
frame5.grid(row=1, column=3, padx=10, pady=10, sticky="nw")
label5 = tk.Label(frame5, text="160")
label5.pack()

# Vortag
frame6 = ttk.LabelFrame(root, text="Vortag", padding=(10,10))
frame6.grid(row=1, column=4, padx=10, pady=10, sticky="nw")
label6 = tk.Label(frame6, text="605")
label6.pack()

# Status
frame7 = ttk.LabelFrame(root, text="Status",padding=(10,10))
frame7.grid(row=1, column=5, padx=10, pady=10, sticky="nw")
label7 = tk.Label(frame7, background='green')
label7.pack()



# Body
# Aktuelle Meldungen-Tabelle
frame8 = ttk.LabelFrame(root, text="Aktuelle Meldungen", padding=(10,10))
frame8.grid(row=2, columnspan=6, padx=10, pady=10, sticky="w")

tree1 = ttk.Treeview(frame8, columns=("Datum und Uhrzeit", "Typnummer","Taktzeit", "Tageszähler", "Chargenzähler", "Gesamtzähler", "Dummy1", "Dummy2"))
tree1['show'] = 'headings'
tree1.heading("#1", text="Datum und Uhrzeit")
tree1.heading("#2", text="Typnummer")
tree1.heading("#3", text="Taktzeit")
tree1.heading("#4", text="Tageszähler")
tree1.heading("#5", text="Chargenzähler")
tree1.heading("#6", text="Gesamtzähler")
tree1.heading("#7", text="Dummy 1")
tree1.heading("#8", text="Dummy 2")

# Konfiguriere einzelne Spalten
tree1.column("#1", anchor="center")
tree1.column("#2", anchor="center", width=80)
tree1.column("#3", anchor="center", width=80)
tree1.column("#4", anchor="center", width=80)
tree1.column("#5", anchor="center", width=100)
tree1.column("#6", anchor="center", width=80)
tree1.column("#7", anchor="center", width=80)
tree1.column("#8", anchor="center", width=80)

# Lade alle Daten von der Datenbank
cur.execute("SELECT datum_uhrzeit,typnummer,taktzeit,tageszaehler,endloszaehler,platzhalter1,platzhalter2,platzhalter3 FROM data ORDER BY datum_uhrzeit DESC")
for row in cur.fetchall():
    tree1.insert("", "end", values=row)

tree1.pack()

# Fehlerliste??? (Zweite Tabelle)
frame9 = ttk.LabelFrame(root, text="Fehlerliste", padding=(10,10))
frame9.grid(row=3, columnspan=6, padx=10, pady=10, sticky="w")

tree2 = ttk.Treeview(frame9, columns=("Datum und Uhrzeit", "Dummy 1","Dummy 2", "Dummy 3", "Dummy 4", "Dummy 5", "Dummy 6", "Fehler", "Warnlampe"))
tree2['show']='headings'
tree2.heading("#1", text="Datum und Uhrzeit")
tree2.heading("#2", text="Dummy 1")
tree2.heading("#3", text="Dummy 2")
tree2.heading("#4", text="Dummy 3")
tree2.heading("#5", text="Dummy 4")
tree2.heading("#6", text="Dummy 5")
tree2.heading("#7", text="Dummy 6")
tree2.heading("#8", text="Fehler")
tree2.heading("#9", text="Warnlampe")

tree2.column("#1", anchor="center")
tree2.column("#2", anchor="center", width=70)
tree2.column("#3", anchor="center", width=70)
tree2.column("#4", anchor="center", width=70)
tree2.column("#5", anchor="center", width=70)
tree2.column("#6", anchor="center", width=70)
tree2.column("#7", anchor="center", width=70)
tree2.column("#8", anchor="center", width=80)
tree2.column("#9", anchor="center", width=80)

tree2.pack()

# Diese Funktion aktualisiert jede Sekunde die Daten in der Liste und damit zugehörigen Infos in der oberen Leiste
def aktualisieren():
    for i in tree1.get_children():
        tree1.delete(i)
    # Lade alle Daten von der Datenbank
    cur.execute("SELECT datum_uhrzeit,typnummer,taktzeit,tageszaehler,endloszaehler,platzhalter1,platzhalter2,platzhalter3 FROM data ORDER BY datum_uhrzeit DESC")
    for row in cur.fetchall():
        tree1.insert("", "end", values=row)

    # Durchschnittstaktzeit berechnen
    cur.execute("SELECT AVG(taktzeit) FROM data")
    average_taktzeit = round(cur.fetchone()[0], 2)
    label2['text'] = str(average_taktzeit)+"s"

    # Damit es sich wiederholt rufen wir die Funktion wieder nach einer Sekunde auf
    root.after(1000, aktualisieren)

root.after(1000, aktualisieren)
root.mainloop()
con.close()