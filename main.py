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

    wait = input("Press enter to continue...")

    func.MenuInterface()
    

    match 


    # userData = func.GetDataFromDB("Gebruiker")

    # Gebruiker1000 = func.IDToObject(userData, 1000 , module.Gebruiker)
    # Fiets1000 = func.IDToObject(func.GetDataFromDB("Fietsen"), 1000, module.Fiets)

    # func.NeemFietss(Gebruiker1000, Fiets1000)






    # users = List[0] # dict of users
    # bikes = List[1] # dict of bikes
    # stations = List[2] # dict of stations
    # print("Users: ", users)
    #print(len(ListOfData[2]))





if __name__ == "__main__":
    Main(len(sys.argv), sys.argv)