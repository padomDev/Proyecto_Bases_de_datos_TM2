from repositories.logs_repo import get_logs_repo


def menu_logs():
    while True:
        print("-------------------------------------------------------------------")
        print("                         MENÚ DE LOGS")
        print("                        1. Consultar logs")
        print("                        2. Volver")
        print("-------------------------------------------------------------------")

        try:
            opcion = int(input("Ingrese una opción: "))

            match opcion:
                case 1:
                    dias = int(input("Ingrese la cantidad de días a consultar: "))

                    if dias <= 0:
                        print("La cantidad de días debe ser mayor que cero")
                        continue

                    logs = get_logs_repo(dias)

                    if not logs:
                        print(f"No hay logs registrados en los últimos {dias} días")
                        continue

                    print("-------------------------------------------------------------------")
                    print(f"Logs de los últimos {dias} días")
                    print("-------------------------------------------------------------------")

                    for log in logs:
                        detalle = ""

                        if log["id_vulnerabilidad"] is not None:
                            detalle = f" | Vulnerabilidad: {log['id_vulnerabilidad']}"
                        elif log["id_mitigacion"] is not None:
                            detalle = f" | Mitigación: {log['id_mitigacion']}"

                        print(
                            f"{log['fecha_hora']} | "
                            f"{log['tipo_evento']} | "
                            f"Usuario: {log['id_usuario']}"
                            f"{detalle}"
                        )

                case 2:
                    return

                case _:
                    print("Opción inválida")

        except ValueError:
            print("El valor ingresado debe ser un número")
