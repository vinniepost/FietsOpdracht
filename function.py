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
            # Default
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
    conn.commit()

    with open("data/stations.json", "r") as f:
        data = json.load(f)
        stations = data["features"]

        i = 1
        for station in stations:
            stationID = station["properties"]["OBJECTID"]
            stationLocation = station["geometry"]
            stationSlotAmount = station["properties"]["Aantal_plaatsen"]
            objectname = "Station" + str(stationID)
            stationsDict[objectname] = module.Station(stationID, stationLocation, stationSlotAmount)
            cur.execute("INSERT INTO Stations VALUES (?, ?, ?)", (stationID, (str(stationLocation["coordinates"][0])+ " " +str(stationLocation["coordinates"][1])), stationSlotAmount))
            conn.commit()
            if i == maximum:
                with open("data/stationDict.json", "w") as f:
                    json.dump(stationsDict, f, cls=module.StationEncoder)
                return stationsDict
            i+=1 
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
# needs update to load with database instead of dataset.json
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
        itemID, itemData = item[0], item[1:]
        if itemID == id:
            return object(item[0],*itemData)
        return None

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

def NeemFietss(Gebruiker:object, Fiets:object):
    # kijk of gebruiker een fiets heeft
    # zo niet, neem fiets
    # zo wel, print error
    
    if (Gebruiker.getGehuurdeFiets() == None):
        Gebruiker.NeemFiets(Fiets)
        Gebruiker.getGehuurdeFiets()
        Fiets.huidigeLokatie = Gebruiker.getNaam()
        Fiets.status = "In gebruik"

        print(Gebruiker.getId())

        conn = ConnectToBD()
        with conn:
            cur = conn.cursor()
            cur.execute("UPDATE Fietsen SET status = ?, Lokatie = ? WHERE id = ?", (Fiets.getStatus(), Fiets.getHuidigeLokatie(), Fiets.getId()))
            conn.commit()
            cur.execute("UPDATE Gebruiker SET gehuurdeFiets = ? WHERE id = ?", (str(Gebruiker.getGehuurdeFiets()), Gebruiker.getId()))
            conn.commit()
        conn.close()


    else:
        print("Gebruiker heeft al een fiets")

