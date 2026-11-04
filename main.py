import os
from utilidades import pedir_numero
from modulo_txt import menu_txt
from modulo_csv import menu_csv


def explorar_directorio():
    ruta = input("Ruta de la carpeta (Enter para usar 'data'): ").strip()
    if ruta == "":
        ruta = "data"

    try:
        archivos = os.listdir(ruta)
    except FileNotFoundError:
        print("Esa carpeta no existe.")
        return
    except NotADirectoryError:
        print("Esa ruta es un archivo, no una carpeta.")
        return

    encontrados = 0
    for nombre in sorted(archivos):
        if nombre.endswith(".txt") or nombre.endswith(".csv"):
            print(f"  - {nombre}")
            encontrados += 1
    if encontrados == 0:
        print("No hay archivos .txt ni .csv en esa carpeta.")


def main():
    os.makedirs("outputs", exist_ok=True)
    opcion = 0
    while opcion != 4:
        print(" EXPLORADOR DE ARCHIVOS ")
        print("1. Explorar directorio")
        print("2. Procesar bitácoras / textos (.txt)")
        print("3. Analizar dataset (.csv)")
        print("4. Salir")
        opcion = pedir_numero("Elija una opción: ", 1, 4)

        if opcion == 1:
            explorar_directorio()
        elif opcion == 2:
            menu_txt()
        elif opcion == 3:
            menu_csv()

    print("Hasta luego")


if __name__ == "__main__":
    main()