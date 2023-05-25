import os
import sys
import function as func
import module

def Init():
    if len(sys.argv) < 2:
        if os.path.exists(".temp"):
            return func.Continiuation()
        else:
            return func.FirstRuntime()
    if (sys.argv[1]=="-s"):
        #simulation mode
        pass
    else:
        print("WIP")



def MoveBike(DictOfBikes:dict,BikeID:str, MoveTo:str):
    # zoek fiets, laad in als object, verander locatie, sla op
    DictOfBikes

    # mag dit via de dict of moet ik dit omzetten naar een objest?
    
def Main(argc:int, argv:list):

    ListOfData = Init()
    with open(".temp", "w") as f:
        f.write("Momenteel nog een lege file om te kijken of de runtime check werkt")
    print('\n')
    wait = input("Press enter to continue...")

    func.MenuInterface()

    
def test():

    func.DBInitialisation()

if __name__ == "__main__":
    Main(len(sys.argv), sys.argv)