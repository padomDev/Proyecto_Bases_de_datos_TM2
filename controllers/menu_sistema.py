from controllers.menu_logs import menu_logs
from controllers.menu_vulnerabilidades import menu_vulnerabilidades


def menu_sistema(id_usuario):
    while True:
        print("-------------------------------------------------------------------")
        print("                        MENÚ DEL SISTEMA")
        print("                    1. Ver vulnerabilidades")
        print("                    2. Consultar logs")
        print("                    3. Cerrar sesión")
        print("-------------------------------------------------------------------")

        try:
            opcion = int(input("Ingrese una opción: "))

            match opcion:
                case 1:
                    menu_vulnerabilidades(id_usuario)
                case 2:
                    menu_logs()
                case 3:
                    return
                case _:
                    print("Opción inválida")

        except ValueError:
            print("El valor ingresado debe ser un número")
