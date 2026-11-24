from controllers.menu_sistema import menu_sistema
from repositories.vulnerabilidades_repo import get_vulnerabilidades_repo, get_mitigaciones_repo

def menu_vulnerabilidades():
    vulnerabilidades = get_vulnerabilidades_repo()

    print("Lista de vulnerabilidades")
    print("--------------------------------")

    for counter, vulnerabilidad in enumerate(vulnerabilidades, start=1):
        print(f'{counter} - {vulnerabilidad["nombre"]}')

    while True:
        try:
            opcion = int(input("Ingrese una opción: "))

            if 1 <= opcion <= len(vulnerabilidades):

                vulnerabilidad = vulnerabilidades[opcion - 1]

                print(f'\nVulnerabilidad: {vulnerabilidad["nombre"]}')
                print(f'CVE: {vulnerabilidad["codigo_cve"]}')
                print(f'Severidad: {vulnerabilidad["severidad"]}')

                mitigaciones = get_mitigaciones_repo(
                    vulnerabilidad["id"]
                )

                print(mitigaciones)

                return

            else:
                print("Opción inválida")

            menu_sistema()

        except ValueError:
            print("El valor ingresado debe ser un número")