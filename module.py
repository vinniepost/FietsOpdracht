import json
from typing import Any
class Station:
    def __init__(self, id, location, capacity):
        self.id = id
        self.location = location
        self.capacity = capacity
        self.availableSlots = [(Slot(self.id,i)=="vrij") for i in range(capacity)]
        self.bikes = []

    def addBike(self, bike):
        if len(self.availableSlots) > 0:
            slot = self.availableSlots.pop()
            bike.setSlot(slot)
            self.bikes.append(bike)
            return True
        else:
            return False

    def removeBike(self, bike):
        if bike in self.bikes:
            slot = bike.getSlot()
            self.availableSlots.append(slot)
            self.bikes.remove(bike)
            return True
        else:
            return False
    
    def getId(self):
        return self.id
    def getLocation(self):
        return self.location
    def getCapacity(self):
        return self.capacity
    def getAvailableSlots(self):
        return self.availableSlots

  
class Slot:
    def __init__(self, slotId, stationId, bikeID="Leeg"):
        self.slotId = slotId
        self.status = "vrij"
        self.stationId = stationId
        self.FietsId = bikeID

    def getId(self):
        return self.slotId

    def getStatus(self):
        return self.status

    def setFietsID(self, NieuweFietsID):
        self.FietsId = NieuweFietsID

    def setStatus(self, newStatus):
        self.status = newStatus

    def ZetFiets(self, bike):
        self.bike = bike
        self.setStatus("bezet")

    def NeemFiets(self):
        self.bike = None
        self.setStatus("vrij")

class Fiets:
    def __init__(self, id, status, lokatie, slotID="n.v.t.", stationID="n.v.t.") -> None:
        self.id = id
        self.status = status
        self.huidigeLokatie = lokatie
        self.slotID = slotID
        self.stationID = stationID

    def __str__(self) -> str:
        return f"Fiets {self.id} is {self.status} en staat op {self.huidigeLokatie}"

    def setStatus(self, status):
        self.status = status
    
    

    def setHuidigeLokatie(self, nieuweLokatie):
        self.huidigeLokatie = nieuweLokatie

    def getId(self):
        return self.id
    def getStatus(self):
        return self.status
    def getHuidigeLokatie(self):
        return self.huidigeLokatie
    def getSlotID(self):
        return self.slotID
    
class Gebruiker:
    def __init__(self, id, naam, geboorteDatum, woonplaats,gehuurdeFiets="None"):
        self.naam = naam
        self.id = id
        self.geboorteDatum = geboorteDatum
        self.woonplaats = woonplaats
        if (self.id == -1):
            self.Fietsen = gehuurdeFiets
        else:
            self.gehuurdeFiets = gehuurdeFiets
    
    def getNaam(self):
        return self.naam
    def getId(self):
        return self.id
    def getGeboorteDatum(self):
        return self.geboorteDatum
    def getWoonplaats(self):
        return self.woonplaats
    def getGehuurdeFiets(self):
        if self.id == -1:
            return self.Fietsen
        else:
            return self.gehuurdeFiets
    
    def NeemFiets(self, fiets):
        if self.id == -1:
            self.Fietsen += "fiets " + str(fiets.getId()) + ", "

        print(f"Fiets{fiets.getId()} is nu in gebruik")
        self.gehuurdeFiets = f"fiets {fiets.getId()}"
        print(f"Fiets {self.gehuurdeFiets} is nu in gebruik")


    def ZetFietsTerug(self, fiets, station):
        if (self.id == -1):
            self.Fietsen = self.Fietsen.replace("fiets " + str(fiets.getId()) + ", ", "")
        else:
            self.gehuurdeFiets = "None"
        print(f"Fiets {fiets.getId()} is nu teruggezet")


class Fietstransporteur(Gebruiker):
    def __init__(self) -> None:
        super().__init__(id=None, geboorteDatum=None, woonplaats=None)
        self.gehuurdeFietsen = []

    def NeemFiets(self, fiets: Fiets):
        self.gehuurdeFiets.append(fiets)

    def ZetFiets(self, fiets:Fiets):
        if fiets in self.gehuurdeFiets:
            self.gehuurdeFiets.remove(fiets)
        else:
            print("Fiets niet in de transportauto")

class Logboek:
    def __init__(self) -> None:
        try:
            with open("/output/data.json", "r") as data:
                self.data = json.load(data)
        except FileNotFoundError:
            with open("/output/data.json", "w") as data:
                self.data = []
                json.dump(self.data, data)
        
    def Log(self, data):
        self.data.append(data)
        with open(self.filepath, "w") as f:
            json.dump(self.data, f)

class StationEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Station):
            # Convert the Station object to a dictionary
            return {
                "id": obj.getId(),
                "location": obj.getLocation(),
                "capacity": obj.getCapacity(),
                "isSlotTaken": obj.getAvailableSlots()
            }
        return super().default(obj)
    
class FietsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Fiets):
            return {
                "id": obj.getId(),
                "status": obj.getStatus(),
                "huidige Lokatie": obj.getHuidigeLokatie()
            }
        return super().default(obj)

class UserEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Gebruiker):
            return{
                "naam": obj.getNaam(),
                "id": obj.getId(),
                "geboorteDatum": obj.getGeboorteDatum(), 
                "woonplaats": obj.getWoonplaats(),
                "gehuurdeFiets": obj.getGehuurdeFiets()
            }
        return super().default(obj)

class GebruikerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Gebruiker):
            return obj.__dict__
        elif isinstance(obj, Station):
            return obj.__dict__
        return super().default(obj)