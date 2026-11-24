from repositories.vulnerabilidades_repo import get_vulnerabilidades_repo, get_mitigaciones_repo
from repositories.logs_repo import log_vulnerabilidad_repo, log_mitigacion_repo


def menu_vulnerabilidades(id_usuario):
    while True:
        vulnerabilidades = get_vulnerabilidades_repo()

        print("-------------------------------------------------------------------")
        print("Lista de vulnerabilidades")

        for contador, vulnerabilidad in enumerate(vulnerabilidades, start=1):
            print(f'{contador}. {vulnerabilidad["nombre"]}')

        print("0. Volver")
        print("-------------------------------------------------------------------")

        try:
            opcion = int(input("Seleccione una vulnerabilidad: "))

            if opcion == 0:
                return

            if 1 <= opcion <= len(vulnerabilidades):
                vulnerabilidad = vulnerabilidades[opcion - 1]
                log_vulnerabilidad_repo(id_usuario, vulnerabilidad["id"])

                print(f'\nVulnerabilidad: {vulnerabilidad["nombre"]}')
                print(f'CVE: {vulnerabilidad["codigo_cve"]}')
                print(f'Severidad: {vulnerabilidad["severidad"]}')
                print(f'Descripción: {vulnerabilidad["descripcion"]}')

                mitigaciones = get_mitigaciones_repo(vulnerabilidad["id"])

                if not mitigaciones:
                    print("No hay mitigaciones registradas")
                    continue

                while True:
                    print("\nMitigaciones:")

                    for contador, mitigacion in enumerate(mitigaciones, start=1):
                        print(
                            f"{contador}. {mitigacion['tipo_mitigacion']} "
                            f"(prioridad {mitigacion['prioridad']})"
                        )

                    print("0. Volver a vulnerabilidades")
                    opcion_mitigacion = int(input("Seleccione una mitigación: "))

                    if opcion_mitigacion == 0:
                        break

                    if 1 <= opcion_mitigacion <= len(mitigaciones):
                        mitigacion = mitigaciones[opcion_mitigacion - 1]
                        print(f"Descripción: {mitigacion['descripcion']}")
                        log_mitigacion_repo(id_usuario, mitigacion["id"])
                    else:
                        print("Opción inválida")

            else:
                print("Opción inválida")

        except ValueError:
            print("El valor ingresado debe ser un número")
