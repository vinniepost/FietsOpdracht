import os
import sys
import module
import json
import random
import sqlite3
from sqlite3 import Error

from random_address import real_random_address as rra

def FirstRuntime():
    """
    Functie die de temp.json aanmaakt om het programma later te laten weten dat het al gerunt heeft.
    """
    logo = """
 ▄█    █▄     ▄████████  ▄█        ▄██████▄          ▄████████ ███▄▄▄▄       ███      ▄█     █▄     ▄████████    ▄████████    ▄███████▄    ▄████████ ███▄▄▄▄   
███    ███   ███    ███ ███       ███    ███        ███    ███ ███▀▀▀██▄ ▀█████████▄ ███     ███   ███    ███   ███    ███   ███    ███   ███    ███ ███▀▀▀██▄ 
███    ███   ███    █▀  ███       ███    ███        ███    ███ ███   ███    ▀███▀▀██ ███     ███   ███    █▀    ███    ███   ███    ███   ███    █▀  ███   ███ 
███    ███  ▄███▄▄▄     ███       ███    ███        ███    ███ ███   ███     ███   ▀ ███     ███  ▄███▄▄▄      ▄███▄▄▄▄██▀   ███    ███  ▄███▄▄▄     ███   ███ 
███    ███ ▀▀███▀▀▀     ███       ███    ███      ▀███████████ ███   ███     ███     ███     ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   ▀█████████▀  ▀▀███▀▀▀     ███   ███ 
███    ███   ███    █▄  ███       ███    ███        ███    ███ ███   ███     ███     ███     ███   ███    █▄  ▀███████████   ███          ███    █▄  ███   ███ 
███    ███   ███    ███ ███▌    ▄ ███    ███        ███    ███ ███   ███     ███     ███ ▄█▄ ███   ███    ███   ███    ███   ███          ███    ███ ███   ███ 
 ▀██████▀    ██████████ █████▄▄██  ▀██████▀         ███    █▀   ▀█   █▀     ▄████▀    ▀███▀███▀    ██████████   ███    ███  ▄████▀        ██████████  ▀█   █▀  
                        ▀                                                                                       ███    ███                                     
"""

    print("\n")
    print(logo)     
    print("\n")

    DBInitialisation()
    UsersToDB(100)

    with open(".temp", "w") as f:
        f.write("Momenteel nog een lege file om te kijken of de runtime check werkt")

def Continiuation():
    i = input("Wil je verder met de vorige simulatie? (Y,n) \n")
    match i:
        case "n":
            # verwijder vorige simulatie
            remover()
            FirstRuntime()
        case _:
            # verder met vorige simulatie
            pass

def remover():
    files = [".temp", "data/naamlijst.json", "data/fietsen.json", "data/stationsDict.json"]
    for file in files:
        if os.path.exists(file):
            os.remove(file)
        else:
            print("The file does not exist")

def GenerateUsers(aantalUsers:int=100):
    try:
        with open("data/names.json") as input:
            with open("data/naamlijst.json", "w") as output:
                Namen = json.load(input)
                JongensNamen = Namen["Mannen_Voornaam"]
                VrouwenNamen = Namen["Vrouwen_Voornaam"]
                Achternamen = Namen["Achternaam"]
            
                rngNamen = []
                i = 1000
                while len(rngNamen) <= (aantalUsers-1):
                    if (len(rngNamen) % 2) == 0:
                        JongensNaam = (JongensNamen[random.randint(0,len(JongensNamen)-1)]+" " + (Achternamen[random.randint(0,len(Achternamen)-1)]))
                        if JongensNaam not in rngNamen:
                            rngNamen.append(JongensNaam)
                    else:
                        MeisjesNaam = (VrouwenNamen[random.randint(0,len(VrouwenNamen)-1)]+" " + (Achternamen[random.randint(0,len(Achternamen)-1)]))
                        if MeisjesNaam not in rngNamen:
                            rngNamen.append(MeisjesNaam)
                outputData = {
                    "Namen": rngNamen
                }
                json.dump(outputData, output)

    except FileNotFoundError:
        print("JSON File not found at \"/data/namen.json \"")

    # class Gebruiker: self, id, geboorteDatum, woonplaats
    n = 1000
    Users = {}
    namenL = outputData["Namen"]
    for i in namenL:
        verjaardag = (random.choice(["01", "02", "03", "04", "05", "06", "07", "08", "09", 
        "10", "11", "12"]) + "/" + random.choice(["01", "02", "03", "04", "05", "06", 
        "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", 
        "20", "21", "22", "23", "24", "25", "26", "27", "28"]) + "/" + 
        random.choice(["1980", "1981", "1982", "1983", "1984", "1985", "1986", 
        "1987", "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1996", 
        "1997", "1998", "1999", "2000"]))
        index = str(i.replace(" ", "")) + str(n)
        Users[index] = module.Gebruiker(n,i,verjaardag,rra()["address1"])
        n+=1
    with open("data/UserData.json", "w") as f:
        json.dump(Users, f, cls=module.UserEncoder)
    return Users

def GenerateTransportator():
    # class Transportator: self, id, geboorteDatum, woonplaats
    Transportator = {}
    Transportator["Transportator"] = module.Transportator(1000, "01/01/2000", rra())
    with open("data/Transportator.json", "w") as f:
        json.dump(Transportator, f, cls=module.TransportatorEncoder)
    return Transportator

def GenerateBike(id, status, lokatie, slotID, stationID):
    # Only generate one bike using the class Fiets
    Fiets = module.Fiets(id, status, lokatie, slotID, stationID)
    conn = ConnectToBD()
    cur = conn.cursor()
    cur.execute("INSERT INTO Fietsen VALUES (?, ?, ?, ?, ?)", (Fiets.id, Fiets.status, Fiets.huidigeLokatie, Fiets.slotID, Fiets.stationID))
    conn.commit()
    conn.close()
    return Fiets

def Add_DB_Entree(table, values):
    conn = ConnectToBD()
    cur = conn.cursor()
    cur.execute("INSERT INTO " + table + " VALUES " + values)

    conn.commit()

def Add_DB_Bulk(conn, table, values):
    for value in values:
        Add_DB_Entree(conn, table, value)

def GetDataFromDB(table) -> list:
    conn = ConnectToBD()
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table)
    data = cur.fetchall()
    return data

def IDToObject(data, id, object):
    for item in data:
        itemID, itemData = str(item[0]), item[1:]
        for entree in item[1:]:
            if type(entree) != str:
                entree = str(entree)

        print(itemID, itemData)
        if str(itemID) == str(id):
            return object(item[0],*itemData)

def Add_DB_User(conn, users):
    conn = ConnectToBD()
    with conn:
        cur = conn.cursor()
        cur.execute("insert into Gebruikers values (?,?,?,?)", users)
        conn.commit()
    conn.close()

def ConnectToBD():
    try:
        conn = sqlite3.connect(r"data/AplicatieDB.sqlite")
        return conn
    except Error:
        print("Error connecting to DB")

def UsersToDB(maxUsers):
    users = GenerateUsers(maxUsers)  
    for user in users:
        print(users[user].getNaam(), users[user].getGeboorteDatum())
        data = f"({str(users[user].getId())}, \"{str(users[user].getNaam())}\", \"{str(users[user].getGeboorteDatum())}\", \"{str(users[user].getWoonplaats())}\", \"{str(users[user].getGehuurdeFiets())}\")"
        Add_DB_Entree("Gebruikers", str(data))

    data = f"({str(-1)}, \"{'Transporteur'}\", \"{'n.v.t'}\", \"{'n.v.t'}\", \"{''}\")"
    Add_DB_Entree("Gebruikers", str(data))
    return users

def NeemFietss(Gebruiker:object, Fiets:object, Station:object):
    conn = ConnectToBD()
    bikeAvelible = False
    
    # TODO: zet hier een try rond
    with conn:
        cur = conn.cursor()
        for slot in cur.execute("SELECT current FROM Sloten WHERE StationID = ?", (Station.id,)):
            if slot[0] == "Bezet":
                bikeAvelible = True
                break

    if ((Gebruiker.getGehuurdeFiets() == "None" or Gebruiker.getId() == -1) and bikeAvelible == True):
        Gebruiker.NeemFiets(Fiets)

        if Gebruiker.getId() != -1:
            Fiets.huidigeLokatie = Gebruiker.getNaam()
            Fiets.status = "In gebruik"
            Fiets.SlotID = "n.v.t."
        with conn:
            cur = conn.cursor()
            cur.execute("UPDATE Fietsen SET status = 'Bezet', Lokatie = ?, SlotID = 'n.v.t.', StationID = 'n.v.t.' WHERE id = ?", (Fiets.getHuidigeLokatie(), Fiets.getId()))
            conn.commit()
            cur.execute("UPDATE Gebruikers SET gehuurdeFiets = ? WHERE id = ?", (str(Gebruiker.getGehuurdeFiets()), Gebruiker.getId()))
            conn.commit()
        conn.close()
    elif (bikeAvelible == False):
        print("Er zijn geen fietsen beschikbaar")
    else:
        print("Gebruiker heeft al een fiets")

def ZetFietsTerug(Gebruiker:object, Station:object, Fiets:object):
    if ((Gebruiker.getGehuurdeFiets() != "None") and (len(Station.availableSlots) > 0)):
        Gebruiker.ZetFietsTerug(Fiets, Station)
        Fiets.huidigeLokatie = f"Station"
        Fiets.status = "Vrij"
        conn = ConnectToBD()
        with conn:
            cur = conn.cursor()
            for i in cur.execute("SELECT id FROM Sloten WHERE current = 'Vrij' AND StationID = ?", (Station.getId(),)):               
                Fiets.slotID = i[0]
                break
            if(Gebruiker.getId() == -1 and Gebruiker.getGehuurdeFiets() == ""):
                Gebruiker.Fietsen = "None"
            cur.execute("UPDATE Fietsen SET status = 'Vrij', Lokatie = ?, SlotID = ?, StationID = ? WHERE id = ?", (Fiets.huidigeLokatie, Fiets.slotID, Station.getId() , Fiets.getId()))
            cur.execute("UPDATE Gebruikers SET gehuurdeFiets = ? WHERE id = ?", (str(Gebruiker.getGehuurdeFiets()), Gebruiker.getId()))
            cur.execute("UPDATE Sloten SET current = 'Bezet', FietsID = ? WHERE id = ?", (Fiets.getId(), Fiets.slotID))
            conn.commit()
        conn.close()
    else:
        print("Gebruiker heeft geen fiets")

def MenuInterface():

    print("welk soort gebruiker bent u?\n1. Gebruiker\n2. Transporteur\nq. Exit")
    keuze = input("\n")

    match keuze:
        case "1":
            print("Welkom gebruiker")
            GebruikerInterface()
        case "2":
            print("Welkom transporteur")
            TransporteurInterface()
        case "q":
            print("Tot ziens")
            exit()
        case _:
            print("Geen geldige keuze")
            MenuInterface()

def FietsIdFromUser(UserId):
    conn = ConnectToBD()
    cur = conn.cursor()
    test = cur.execute("SELECT naam FROM Gebruikers WHERE id = ?", (UserId,))
    with conn:
        cur = conn.cursor()
        gehuurdeFiets =  cur.execute("SELECT gehuurdeFiets FROM Gebruikers WHERE id = ?", (UserId,))
        if (gehuurdeFiets[0] == "None"):
            print("Gebruiker heeft geen fiets")
        else:
            pass

def FietsIDGetter(StationId):
    conn = ConnectToBD()
    cur = conn.cursor()
    cur.execute("SELECT current FROM Sloten WHERE StationID = ?", (StationId,))
    with conn:
        cur = conn.cursor()
        for i in cur.execute("SELECT current, id FROM Sloten WHERE StationID = ?", (StationId,)):
            if i[0] == "Bezet":
                cur.execute("SELECT FietsID FROM Sloten WHERE StationID = ? AND id = ?", (StationId,i[1]))
                FietsID = cur.fetchone()[0]
                cur.execute("UPDATE Sloten SET current = ?, FietsID = 'Leeg' WHERE FietsID = ?", ("Vrij", FietsID))
                return FietsID

def GebruikerInterface():
    print("1. Fiets ontlenen\n2. Fiets terug zetten\n3. Status fiets met id\
          \n4. Status slots in station\n5. Status Gebruiker met id\nq. Exit")
    keuze = input("\n")

    match keuze:
        case "1":
            print("Fiets ontlenen: Geef GebruikerID en FietsID")
            GebruikerID = input("GebruikerID: ")
            StationID = input("StationID: ")
            FietsID = FietsIDGetter((StationID))
            userdata = GetDataFromDB("Gebruikers")
            fietsdata = GetDataFromDB("Fietsen")
            stationdata = GetDataFromDB("Stations")
            Gebruiker = IDToObject(userdata, GebruikerID, module.Gebruiker)
            Fiets = IDToObject(fietsdata, FietsID, module.Fiets)
            Station = IDToObject(stationdata, StationID, module.Station)
            NeemFietss(Gebruiker, Fiets, Station)
            GebruikerInterface()
        case "2":
            print("Fiets terug Zetten")
            GebruikerID = input("GebruikerID: ")
            StationID = input("StationID: ")
            BikeID = input("FietsID: ")
            userdata = GetDataFromDB("Gebruikers")
            stationdata = GetDataFromDB("Stations")
            bikeData = GetDataFromDB("Fietsen")
            Gebruiker = IDToObject(userdata, GebruikerID, module.Gebruiker)
            Station = IDToObject(stationdata, StationID, module.Station)
            Fiets = IDToObject(bikeData, BikeID, module.Fiets)
            ZetFietsTerug(Gebruiker, Station, Fiets)
            GebruikerInterface()
        case "3":
            print("Status fiets met id")
            FietsStatusViaID()
            GebruikerInterface()
        case "4": # TODO: fix
            print("\nStatus slots in station\n")
            StationID = input("StationID: ")
            conn = ConnectToBD()
            cur = conn.cursor()
            with conn:
                cur = conn.cursor()
                for i in cur.execute("SELECT id, current FROM Sloten WHERE StationID = ?", (StationID,)):
                    print(i)
            conn.commit()
            conn.close()
            GebruikerInterface()
        case "5":
            print("Status Gebruiker met id")
            GebruikerID = input("GebruikerID: ")
            userdata = GetDataFromDB("Gebruikers")
            Gebruiker = IDToObject(userdata, GebruikerID, module.Gebruiker)
            print(Gebruiker.getGehuurdeFiets())
            GebruikerInterface()
        case "q":
            print("Tot ziens")
        case _:
            print("Geen geldige keuze")
            GebruikerInterface()

def GenerateSlot(stationId, totaalAantalSloten):
    Slot = module.Slot(totaalAantalSloten,stationId)
    return Slot

def DBInitialisation():
    try:
        print("Generating data and saving it to the database")
        stationDict = {}
        totaalAantalFietsen = 0
        totaalAantalSloten = 0
        conn = ConnectToBD()
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Gebruikers")
        cur.execute("DROP TABLE IF EXISTS Fietsen")
        cur.execute("DROP TABLE IF EXISTS Sloten")
        cur.execute("DROP TABLE IF EXISTS Stations")
        cur.execute("CREATE TABLE Fietsen (id INTEGER PRIMARY KEY, status TEXT, Lokatie TEXT, SlotID INTEGER, StationID INTEGER, FOREIGN KEY(SlotID) REFERENCES Sloten(id), FOREIGN KEY(StationID) REFERENCES Stations(id))")
        cur.execute("CREATE TABLE Gebruikers (id INTEGER PRIMARY KEY, naam TEXT, geboorteDatum TEXT, woonplaats TEXT, gehuurdeFiets TEXT)")
        cur.execute("CREATE TABLE Sloten (id INTEGER PRIMARY KEY, current TEXT, FietsID TEXT,StationID INTEGER,FOREIGN KEY(StationID) REFERENCES Stations(id))")
        cur.execute("CREATE TABLE Stations (id INTEGER PRIMARY KEY, Lokatie TEXT, Capasiteit INTEGER)")
        with open("data/stations.json") as f:
            data = json.load(f)
            stations = data["features"]
            SurfixId = 1 # niet zeker
            slotID = 1

            for station in stations:
                print(f"Generating station {SurfixId}/{len(stations)}, may take a second", end='\r')
                huidigAantalSlots = 0
                stationId = station["properties"]["OBJECTID"]
                stationLokatie = (str(station["geometry"]["coordinates"][0])+","+str(station["geometry"]["coordinates"][1]))
                stationCapasiteit = station["properties"]["Aantal_plaatsen"]
                objectNaam = "Station" + str(SurfixId)
                stationDict[objectNaam] = module.Station(stationId,stationLokatie,stationCapasiteit)
                cur.execute("INSERT INTO Stations (id, Lokatie, Capasiteit) VALUES (?,?,?)",(stationId,stationLokatie,stationCapasiteit))
                conn.commit()
                SurfixId += 1
                for i in range(stationCapasiteit):
                    Slot = GenerateSlot(totaalAantalSloten, stationId)
                    totaalAantalSloten += 1
                    huidigAantalSlots += 1
                    slotBezet = "Vrij"
                    if (huidigAantalSlots <= stationCapasiteit/2):
                        Fiets = GenerateBike((totaalAantalFietsen+1000),"Vrij","Station", slotID,stationId)
                        Slot.setFietsID(Fiets.id)
                        totaalAantalFietsen += 1
                        slotBezet = "Bezet"
                    slotID += 1
                    cur = conn.cursor()
                    cur.execute("INSERT INTO Sloten (id, current, FietsID ,StationID) VALUES (?,?,?,?)",(totaalAantalSloten,slotBezet,Slot.FietsId,stationId))
                    conn.commit()
        conn.close()
    except Error as e:
        print(e)
        print("Error in DBInitialisation")

def FietsStatusViaID():
    try:
        FietsID = input("FietsID: ")
        fietsdata = GetDataFromDB("Fietsen")
        Fiets = IDToObject(fietsdata, FietsID, module.Fiets)
        print(Fiets.getStatus())
    except Error as e:
        print(e)
        print("Error in FietsStatusViaID")

def TransporteurInterface():
    print("1. Fiets ontlenen\n2. Fiets terug zetten \nq. Exit")
    keuze = input("\n")

    match keuze:
        case "1":
            print("Fiets ontlenen: Geef GebruikerID en FietsID")
            GebruikerID = '-1'
            StationID = input("StationID: ")
            FietsID = FietsIDGetter((StationID))
            userdata = GetDataFromDB("Gebruikers")
            fietsdata = GetDataFromDB("Fietsen")
            stationdata = GetDataFromDB("Stations")
            Gebruiker = IDToObject(userdata, GebruikerID, module.Gebruiker)
            Fiets = IDToObject(fietsdata, FietsID, module.Fiets)
            Station = IDToObject(stationdata, StationID, module.Station)
            NeemFietss(Gebruiker, Fiets, Station)
            TransporteurInterface()
        case "2":
            print("Fiets terug Zetten")
            GebruikerID = '-1'
            StationID = input("StationID: ")
            BikeID = input("FietsID: ")
            userdata = GetDataFromDB("Gebruikers")
            stationdata = GetDataFromDB("Stations")
            bikeData = GetDataFromDB("Fietsen")
            Gebruiker = IDToObject(userdata, GebruikerID, module.Gebruiker)
            Station = IDToObject(stationdata, StationID, module.Station)
            Fiets = IDToObject(bikeData, BikeID, module.Fiets)
            ZetFietsTerug(Gebruiker, Station, Fiets)
            TransporteurInterface()
        case "q":
            print("Tot ziens")
        case _:
            print("Geen geldige keuze")
            TransporteurInterface()