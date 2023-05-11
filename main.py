####
## imports
####
import os
import sys
import module
import json
import random

####
## functions
####
def Init():
    if os.path.exists("temp.json"):
        ContiniueRuntime()
    else:
        FirstRuntime()


def MoetNogNaamVerzinnen():
    """
    Deel dat zowel in first als erna gebruikt wordt
    """
    try:
        with open("/data/dataset.json" "r") as f:
            data = f
    except FileNotFoundError:
        print("No data found at \"/data/dataset.json\"")
    pass


def FirstRuntime():
    """
    Functie die de temp.json aanmaakt om het programma later te laten weten dat het al gerunt heeft.
    """
    with open("temp.json", "w") as f:
        f.write("Momenteel nog een lege file om te kijken of de runtime check werkt")
    
    # genereer naamlijst
    with open("data/names.json") as input:
        with open("data/naamlijst.json", "w") as output:
            Namen = json.load(input)
            JongensNamen = Namen["Mannen_Voornaam"]
            VrouwenNamen = Namen["Vrouwen_Voornaam"]
            Achternamen = Namen["Achternaam"]
            
            rngNamen = []
            while len(rngNamen) < 55000:
                JongensNaam = (JongensNamen[random.randint(0,len(JongensNamen)-1)]+" " + (Achternamen[random.randint(0,len(Achternamen)-1)]))
                if JongensNaam not in rngNamen:
                    rngNamen.append(JongensNaam)
                MeisjesNaam = (VrouwenNamen[random.randint(0,len(VrouwenNamen)-1)]+" " + (Achternamen[random.randint(0,len(Achternamen)-1)]))
                if MeisjesNaam not in rngNamen:
                    rngNamen.append(MeisjesNaam)
            print(len(rngNamen))
            json.dump(rngNamen, output)






    

def ContiniueRuntime():
    i = input("Wil je verder met de vorige simulatie? (Y,n)")
    match i:
        case "n":
            # verwijder vorige simulatie
            os.remove("temp.json")
            os.remove("data/naamlijst.json")
        case _:
            # Default
            pass


def GenerateUsers():
    try:
        with open("/data/namen.json", "r") as f:
            jongensnamen = "Something"
        pass

    except FileNotFoundError:
        print("JSON File not found at \"/data/namen.json \"")


def ResetRuntime():
    pass


## temp
def UserInterface():
    pass


def Main():
    FirstRuntime()


if __name__ == "__main__":
    Main()