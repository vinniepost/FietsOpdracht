import os
import sys
import function as func


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
    
def Main(argc:int, argv:list):

    Init()
    with open(".temp", "w") as f:
        f.write("Momenteel nog een lege file om te kijken of de runtime check werkt")
    print('\n')
    input("Press enter to continue...")

    func.MenuInterface()

if __name__ == "__main__":
    Main(len(sys.argv), sys.argv)