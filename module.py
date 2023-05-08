# classes


class Stations:
    def __init__(self, location, capacity):
        self.location = location
        self.capacity = capacity
        self.availableSlots = [Slot(i) for i in range(capacity)]
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


class Slot:
    def __init__(self, slotId):
        self.slotId = slotId
        self.status = "vrij"
        self.fiets = None

    def getId(self):
        return self.slotId

    def getStatus(self):
        return self.status

    def setStatus(self, newStatus):
        self.status = newStatus

    def ZetFiets(self, bike):
        self.bike = bike
        self.setStatus("bezet")

    def NeemFiets(self):
        self.bike = None
        self.setStatus("vrij")


class Fiets:
    def __init__(self, ID, status, huidigeLokatie) -> None:
        self.id = ID
        self.status = status
        self.huidigeLokatie = huidigeLokatie

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
    


class Gebruiker:
    def __init__(self) -> None:
        pass


class Fietstransporteur:
    def __init__(self) -> None:
        pass


class Logboek:
    def __init__(self) -> None:
        pass
