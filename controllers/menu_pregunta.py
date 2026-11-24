def menu_pregunta(pregunta):
    while True:
        print("                 ", pregunta["pregunta"])
        print("-------------------------------------------------------------------")

        letras = "ABCD"
        respuestas = pregunta["respuestas"]

        for letra, respuesta in zip(letras, respuestas):
            print(f"{letra}. {respuesta['texto']}")

        print("-------------------------------------------------------------------")

        opcion = input("Ingrese una respuesta: ").strip().upper()

        if opcion not in letras[:len(respuestas)]:
            print("Respuesta inválida")
            continue

        posicion = letras.index(opcion)
        return respuestas[posicion]["id"]
