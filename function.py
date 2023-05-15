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

    maxUser = int(input(" Hoeveel gebruikers wil je genereren? \n"))
    maxBikes = int(input(" Hoeveel fietsen wil je genereren? (max 8999) \n"))
    maxStations = int(input(" Hoeveel stations wil je genereren? (max 309) \n"))

    with open(".temp", "w") as f:
        f.write("Momenteel nog een lege file om te kijken of de runtime check werkt")

    return combineInfo(maxUser, maxBikes, maxStations)

def Continiuation():
    i = input("Wil je verder met de vorige simulatie? (Y,n) \n")
    match i:
        case "n":
            # verwijder vorige simulatie
            remover()
            FirstRuntime()
            return LoadPrevious()
        case _:
            # Default (not needed anymore???)
            return LoadPrevious()

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

def GenerateStations(maximum):
    stationsDict = {}  
    conn = ConnectToBD()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Stations")
    cur.execute("CREATE TABLE Stations (id INTEGER PRIMARY KEY, Lokatie TEXT, Capasiteit INTEGER)")
    cur.execute("DROP TABLE IF EXISTS Slots")
    cur.execute("CREATE TABLE Slots (id INTEGER PRIMARY KEY, current TEXT,StationID INTEGER,FOREIGN KEY(StationID) REFERENCES Stations(id))")
    conn.commit()
    with open("data/stations.json", "r") as f:
        data = json.load(f)
        stations = data["features"]
        i = 1
        CurrentAmountOfSlots = 0
        for station in stations:
            conn = ConnectToBD()
            cur = conn.cursor()
            stationID = station["properties"]["OBJECTID"]
            stationLocation = station["geometry"]
            stationSlotAmount = station["properties"]["Aantal_plaatsen"]
            objectname = "Station" + str(stationID)
            stationsDict[objectname] = module.Station(stationID, stationLocation, stationSlotAmount)
            cur.execute("INSERT INTO Stations VALUES (?, ?, ?)", (stationID, (str(stationLocation["coordinates"][0])+ " " +str(stationLocation["coordinates"][1])), stationSlotAmount))
            conn.commit()
            conn.close()
            print(" Generating slots for stations, May take a second") 
            for slot in range(stationSlotAmount):
                GenerateSlots(stationID, CurrentAmountOfSlots)
                CurrentAmountOfSlots += 1
            if i == maximum:
                with open("data/stationDict.json", "w") as f:
                    json.dump(stationsDict, f, cls=module.StationEncoder)
                return stationsDict
            i+=1

def GenerateSlots(stationID,CurrentAmountOfSlots):
    slot = module.Slot(CurrentAmountOfSlots, stationID)
    conn = ConnectToBD()
    cur = conn.cursor()
    cur.execute("INSERT INTO Slots VALUES (?, ?, ?)", (CurrentAmountOfSlots, str(slot.status), stationID))
    conn.commit()
    conn.close()

def GenerateBikes(max = 4200):
    bikesDir = {}    
    if max > 10000:
        print("To many bikes, max is 8999")
    else:
        conn = ConnectToBD()
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Fietsen")
        cur.execute("CREATE TABLE Fietsen (id INTEGER PRIMARY KEY, status TEXT, Lokatie TEXT)")
        conn.commit()

        for i in range(max):
            bikeId = (1000 + i)
            bikeStatus = "Vrij"
            bikeLocation = "Base"

            cur.execute("INSERT INTO Fietsen VALUES (?, ?, ?)", (bikeId, bikeStatus, bikeLocation))
            conn.commit()
            bikesDir[f"Fiets{bikeId}"] = {
                "id": bikeId,
                "status": bikeStatus,
                "Lokatie": bikeLocation
            }
        conn.close()

    with open("data/fietsen.json", "w") as f:
        json.dump(bikesDir, f, cls=module.FietsEncoder)
    return bikesDir

def LoadPrevious():
    with open("data/dataset.json", "r") as f:
        data = json.load(f)
        List = [data["users"], data["bikes"], data["stations"]]
    return List

def combineInfo(maxUser, maxBikes, maxStations):
    users = UsersToDB(maxUser)
    bikes = GenerateBikes(maxBikes)
    stations = GenerateStations(maxStations)

    data = {
        "users": users,
        "bikes": bikes,
        "stations": stations
    }

    with open("data/dataset.json", "w") as file:
        json.dump(data, file, cls=module.GebruikerEncoder)
    return data

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

def StationsToDB(conn, maxStations):
    conn = ConnectToBD()
    with conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Station")
        cur.execute("CREATE TABLE Station (id INTEGER PRIMARY KEY, locatie TEXT, aantalPlaatsen INTEGER)")
        conn.commit()

        stations = GenerateStations(maxStations)

        for station in stations:
            data = f"({stations[station].getId()}, {stations[station].getLocatie()}, {stations[station].getAantalPlaatsen()})"
            Add_DB_Entree(conn, "Station", data)
    conn.close()

def Add_DB_User(conn, users):
    conn = ConnectToBD()
    with conn:
        cur = conn.cursor()
        cur.execute("insert into Gebruiker values (?,?,?,?)", users)
        conn.commit()
    conn.close()

def ConnectToBD():
    try:
        conn = sqlite3.connect(r"data/AplicatieDB.sqlite")
        return conn
    except Error:
        print("Error connecting to DB")

def UsersToDB(maxUsers):
    conn = ConnectToBD()
    with conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Gebruiker")
        cur.execute("CREATE TABLE Gebruiker (id INTEGER PRIMARY KEY, naam TEXT, geboorteDatum TEXT, woonplaats TEXT, gehuurdeFiets TEXT)")
        conn.commit()

        users = GenerateUsers(maxUsers)
        
        for user in users:
            print(users[user].getNaam(), users[user].getGeboorteDatum())
            data = f"({str(users[user].getId())}, \"{str(users[user].getNaam())}\", \"{str(users[user].getGeboorteDatum())}\", \"{str(users[user].getWoonplaats())}\", \"{str(users[user].getGehuurdeFiets())}\")"
            Add_DB_Entree("Gebruiker", str(data))

    conn.close()
    return users

def NeemFietss(Gebruiker:object, Fiets:object, Station:object):
    conn = ConnectToBD()
    bikeAvelible = False
    with conn:
        cur = conn.cursor()
        for slot in cur.execute("SELECT current FROM Slots WHERE StationID = ?", (Station.id,)):
            print(slot[0])
            if slot != "vrij":
                bikeAvelible = True
                break
    if (Gebruiker.getGehuurdeFiets() == "None" and bikeAvelible == True):
        Gebruiker.NeemFiets(Fiets)
        print(Gebruiker.gehuurdeFiets)
        Fiets.huidigeLokatie = Gebruiker.getNaam()
        Fiets.status = "In gebruik"

        with conn:
            cur = conn.cursor()
            cur.execute("UPDATE Fietsen SET status = ?, Lokatie = ? WHERE id = ?", (Fiets.getStatus(), Fiets.getHuidigeLokatie(), Fiets.getId()))
            conn.commit()
            cur.execute("UPDATE Gebruiker SET gehuurdeFiets = ? WHERE id = ?", (str(Gebruiker.getGehuurdeFiets()), Gebruiker.getId()))
            conn.commit()
        conn.close()
    elif (bikeAvelible == False):
        print("Er zijn geen fietsen beschikbaar")
    else:
        print("Gebruiker heeft al een fiets")

def ZetFietsTerug(Gebruiker:object, Station:object, Fiets:object):
    if (Gebruiker.gehuurdeFiets != "None"):
        Gebruiker.ZetFietsTerug(Fiets)
        Fiets.huidigeLokatie = f"Station {Station.id}"
        Fiets.status = "Vrij"
        conn = ConnectToBD()
        with conn:
            cur = conn.cursor()
            cur.execute("UPDATE Fietsen SET status = ?, Lokatie = ? WHERE id = ?", (Fiets.status, Fiets.huidigeLokatie, Fiets.id))
            cur.execute("UPDATE Gebruiker SET gehuurdeFiets = ? WHERE id = ?", (str(Gebruiker.getGehuurdeFiets()), Gebruiker.getId()))
            conn.commit()
        conn.close()
    else:
        print("Gebruiker heeft geen fiets")
        print(Gebruiker.gehuurdeFiets)

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

def GebruikerInterface():
    print("1. Fiets ontlenen\n2. Fiets terug zetten\n3. Status fiets met id\
          \n4. Status slots in station\n5. Status Gebruiker met id\nq. Exit")
    keuze = input("\n")

    match keuze:
        case "1":
            print("Fiets ontlenen: Geef GebruikerID en FietsID")
            GebruikerID = input("GebruikerID: ")
            FietsID = input("FietsID: ")
            StationID = input("StationID: ")
            userdata = GetDataFromDB("Gebruiker")
            print(userdata)
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
            userdata = GetDataFromDB("Gebruiker")
            stationdata = GetDataFromDB("Stations")
            bikeData = GetDataFromDB("Fietsen")
            Gebruiker = IDToObject(userdata, GebruikerID, module.Gebruiker)
            Station = IDToObject(stationdata, StationID, module.Station)
            Fiets = IDToObject(bikeData, BikeID, module.Fiets)
            ZetFietsTerug(Gebruiker, Station, Fiets)
            GebruikerInterface()
        case "3":
            print("Status fiets met id")
            FietsID = input("FietsID: ")
            fietsdata = GetDataFromDB("Fietsen")
            Fiets = IDToObject(fietsdata, FietsID, module.Fiets)
            print(Fiets.getStatus())
            GebruikerInterface()
        case "4": # TODO: fix
            print("Status slots in station")
            StationID = input("StationID: ")
            stationdata = GetDataFromDB("Stations")
            Station = IDToObject(stationdata, StationID, module.Station)
            print(Station.getSlots())
            GebruikerInterface()
        case "5":
            print("Status Gebruiker met id")
            GebruikerID = input("GebruikerID: ")
            userdata = GetDataFromDB("Gebruiker")
            Gebruiker = IDToObject(userdata, GebruikerID, module.Gebruiker)
            print(Gebruiker.getStatus())
            GebruikerInterface()
        case "q":
            print("Tot ziens")
        case _:
            print("Geen geldige keuze")
            GebruikerInterface()