from services.auth_service import registro_service, login_service
from config.conexion import inicializar_db
from repositories.preguntas_repo import obtener_pregunta_aleatoria_repo
from repositories.usuarios_repo import buscar_usuario
from controllers.menu_pregunta import menu_pregunta
from controllers.menu_sistema import menu_sistema

def menu_ingreso():

    while True:

        print("-------------------------------------------------------------------")
        print("                           1. Registrarse                 ")
        print("                            2. Loguarse                   ")
        print("                             3. Salir                 ")
        print("-------------------------------------------------------------------")

        try:
            opcion = int(input("                        Ingtrese una opcion: "))
            print("-------------------------------------------------------------------")

            match opcion :

                case 1 :
                    usuario = input("                      Ingrese nombre de usuario: ")
                    print("-------------------------------------------------------------------")
                    contraseña = input("                        Ingrese contraseña: ")
                    print("-------------------------------------------------------------------")
                    confirm_contraseña = input("                      Ingrese nuevamente la contraseña: ")
                    print("-------------------------------------------------------------------")
                    pregunta = obtener_pregunta_aleatoria_repo()

                    if pregunta is None:
                        print("No hay preguntas registradas en la base de datos")
                        continue

                    respuesta = menu_pregunta(pregunta)
                    print("-------------------------------------------------------------------")
                    registro = registro_service(
                        usuario, 
                        contraseña, 
                        confirm_contraseña, 
                        pregunta, 
                        respuesta
                        )
                    if registro != True:    
                        for mensaje in registro:
                            print(mensaje)
                    else:
                        print(f"        Registro realizado con exito, bienvenido al club, {usuario}")
                        usuario_db = buscar_usuario(usuario)
                        menu_sistema(usuario_db["id"])


                case 2 :
                    usuario = input("                     Ingrese nombre de usuario: ")
                    print("-------------------------------------------------------------------")
                    contraseña = input("                        Ingrese contraseña: ")
                    print("-------------------------------------------------------------------")
                    pregunta = obtener_pregunta_aleatoria_repo()

                    if pregunta is None:
                        print("No hay preguntas registradas en la base de datos")
                        continue

                    respuesta = menu_pregunta(pregunta)
                    logueo = login_service(
                        usuario, 
                        contraseña, 
                        pregunta, 
                        respuesta
                        )
                    if logueo != True:    
                        for mensaje in logueo:
                            print(mensaje)
                    else:
                        print(f"         Login realizado con exito, bienvenido al club, {usuario}")
                        usuario_db = buscar_usuario(usuario)
                        menu_sistema(usuario_db["id"])
                
                case 3 :
                    return

                case _ :
                    print("-------------------------------------------------------------------")
                    print("Opcion invalida")
                    print("-------------------------------------------------------------------")

        except ValueError:
            print("El valor ingresado debe ser un número")


if __name__ == "__main__":
    inicializar_db()
    menu_ingreso()
