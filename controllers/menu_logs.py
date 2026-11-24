from controllers.menu_sistema import menu_sistema

def menu_logs():
    print("--------------------------------")
    print("          1. Salir")
    print("--------------------------------")
    
    while True:
        try:
            opcion = int(input("Ingrese una opcion: "))

            match opcion :

                    case 1 :
                        menu_sistema()
                    
                    case _ :
                        print("-------------------------------------------------------------------")
                        print("Opcion invalida")
                        print("-------------------------------------------------------------------")

        except ValueError:
            print("El valor ingresado debe ser un número")



#python -m venv venv
#venv\Scripts\activate
#python -m pip install pyinstaller
#pyinstaller --onefile menues.py
