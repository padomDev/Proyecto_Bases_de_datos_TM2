def menu_pregunta(pregunta):

    while True:

        print("                 ", pregunta["pregunta"])
        print("-------------------------------------------------------------------")
        print(pregunta["opcion 1"])
        print(pregunta["opcion 2"])
        print(pregunta["opcion 3"])
        print(pregunta["opcion 4"])
        print("-------------------------------------------------------------------")

        try:

            respuesta = str(input("                     Ingrese una respuesta: "))

            if respuesta not in ["A", "B", "C", "D"]:
                print("-------------------------------------------------------------------")
                print("                         Respuesta invalida")
                print("-------------------------------------------------------------------")
                menu_pregunta(pregunta)

            return respuesta
            
        except ValueError:
            print("Se debe ingresar una letra mayuscula de la A a la D")