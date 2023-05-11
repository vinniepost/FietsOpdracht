####
## imports
####
import os
import sys
import module
import json
import random
from random_address import real_random_address as rra

####
## functions
####
def Init():
    if len(sys.argv) < 2:
        if os.path.exists(".temp"):
            return Continiuation()
        else:
            return FirstRuntime()
    if (sys.argv[1]=="-s"):
        #simulation mode
        pass
    else:
        print("WIP")

####
## terminal things
####

def FirstRuntime():
    """
    Functie die de temp.json aanmaakt om het programma later te laten weten dat het al gerunt heeft.
    """
    maxUser = int(input(" Hoeveel gebruikers wil je genereren?\n"))
    maxBikes = int(input(" Hoeveel fietsen wil je genereren? (max 8999)\n"))
    maxStations = int(input(" Hoeveel stations wil je genereren? (max 309)\n"))

    with open(".temp", "w") as f:
        f.write("Momenteel nog een lege file om te kijken of de runtime check werkt")

    return combineInfo(maxUser, maxBikes, maxStations)

def Continiuation():
    i = input("Wil je verder met de vorige simulatie? (Y,n)")
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
    os.remove(".temp")
    os.remove("data/naamlijst.json")
    os.remove("data/stationDict.json")
    os.remove("data/dataset.json")
    os.remove("data/fietsen.json")

####
## data part
####

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
                while len(rngNamen) < (aantalUsers-1):
                    JongensNaam = (JongensNamen[random.randint(0,len(JongensNamen)-1)]+" " + (Achternamen[random.randint(0,len(Achternamen)-1)]))
                    if JongensNaam not in rngNamen:
                        rngNamen.append(JongensNaam)
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
    namen = outputData["Namen"]
    for i in namen:
        verjaardag = (random.choice(["01", "02", "03", "04", "05", "06", "07", "08", "09", 
        "10", "11", "12"]) + "/" + random.choice(["01", "02", "03", "04", "05", "06", 
        "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", 
        "20", "21", "22", "23", "24", "25", "26", "27", "28"]) + "/" + 
        random.choice(["1980", "1981", "1982", "1983", "1984", "1985", "1986", 
        "1987", "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1996", 
        "1997", "1998", "1999", "2000"]))
        Users[i] = module.Gebruiker(n,verjaardag,rra())
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

    with open("data/stations.json", "r") as f:
        data = json.load(f)
        stations = data["features"]

        i = 0
        while i < maximum:
            for station in stations:
                stationID = station["properties"]["OBJECTID"]
                stationLocation = station["geometry"]
                stationSlotAmount = station["properties"]["Aantal_plaatsen"]
                objectname = "Station" + str(stationID)

                
                stationsDict[objectname] = module.Station(stationID, stationLocation, stationSlotAmount)
                i+=1

    with open("data/stationDict.json", "w") as f:
        json.dump(stationsDict, f, cls=module.StationEncoder)
    return stationsDict

def GenerateBikes(max = 4200):
    bikesDir = {}
    
    if max > 10000:
        print("To many bikes, max is 8999")
    else:
        for i in range(max):
            bikeId = 1000 + i
            bikeStatus = "Vrij"
            bikeLocation = ""
            bikesDir[f"Fiets{bikeId}"] = {
                "id": bikeId,
                "status": bikeStatus,
                "huidige Lokatie": bikeLocation
            }
    with open("data/fietsen.json", "w") as f:
        json.dump(bikesDir, f, cls=module.FietsEncoder)
    return bikesDir

def LoadPrevious():
    with open("data/dataset.json", "r") as f:
        data = json.load(f)
        List = [data["users"], data["bikes"], data["stations"]]
    return List

def combineInfo(maxUser, maxBikes, maxStations):
    users = GenerateUsers(maxUser)
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

def Main():
    List = Init()
    users = List[0]
    bikes = List[1]
    stations = List[2]

    print("Users: ", users)

if __name__ == "__main__":
    Main()