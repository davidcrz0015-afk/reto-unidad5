import matplotlib.pyplot as plt
from utilidades import pedir_numero, obtener_cantidad, guardar_grafico

CONECTORES = ["el", "la", "los", "las", "de", "del", "y", "a", "en", "que", "un",
              "una", "por", "con", "para", "se", "su", "al", "lo", "es", "no", "o",
              "the", "and", "of", "to", "in", "is", "it", "that", "for"]


def leer_lineas(ruta):
    """Lee un archivo de texto y devuelve una lista con sus líneas."""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return archivo.readlines()
    except FileNotFoundError:
        print("Error: no se encontró el archivo.")
    except UnicodeDecodeError:
        print("Error: el archivo no está en formato UTF-8.")
    return []


def contar_palabras(lineas):
    """Cuenta cuántas veces aparece cada palabra (sin conectores)."""
    conteo = {}
    for linea in lineas:
        for palabra in linea.lower().split():
            palabra = palabra.strip(".,;:!?¡¿\"'()[]-")
            if palabra.isalpha() and palabra not in CONECTORES:
                conteo[palabra] = conteo.get(palabra, 0) + 1
    return conteo


def top_palabras(lineas, cantidad):
    """Devuelve las 'cantidad' palabras más repetidas como lista de tuplas."""
    conteo = contar_palabras(lineas)
    ordenadas = sorted(conteo.items(), key=obtener_cantidad, reverse=True)
    return ordenadas[:cantidad]


def resumen_texto(lineas):
    con_espacios = 0
    sin_espacios = 0
    for linea in lineas:
        texto = linea.rstrip("\n")
        con_espacios += len(texto)
        sin_espacios += len(texto.replace(" ", ""))

    print(f"\nTotal de líneas: {len(lineas)}")
    print(f"Caracteres con espacios: {con_espacios}")
    print(f"Caracteres sin espacios: {sin_espacios}")
    print("Top 5 palabras más repetidas:")
    for palabra, veces in top_palabras(lineas, 5):
        print(f"  {palabra}: {veces}")


def extraer_patrones(lineas):
    patron = input("Patrón a buscar (ej. ERROR, 404): ").strip()
    if patron == "":
        print("No escribió ningún patrón.")
        return

    coincidencias = []
    for linea in lineas:
        if patron.lower() in linea.lower():
            coincidencias.append(linea)

    print(f"Se encontraron {len(coincidencias)} líneas con '{patron}'.")
    with open("outputs/coincidencias.txt", "w", encoding="utf-8") as salida:
        salida.writelines(coincidencias)
    print("Las líneas encontradas se guardaron en outputs/coincidencias.txt")


def grafico_palabras(lineas):
    top = top_palabras(lineas, 10)
    if len(top) == 0:
        print("No hay palabras para graficar.")
        return

    palabras = []
    cantidades = []
    for palabra, veces in top:
        palabras.append(palabra)
        cantidades.append(veces)
    palabras.reverse()
    cantidades.reverse()

    plt.figure(figsize=(8, 5))
    plt.barh(palabras, cantidades, color="steelblue")
    plt.title("Top 10 palabras más frecuentes")
    plt.xlabel("Frecuencia")
    plt.ylabel("Palabra")
    guardar_grafico("grafico1_palabras.png")


def grafico_longitudes(lineas):
    longitudes = []
    for linea in lineas:
        longitudes.append(len(linea.rstrip("\n")))

    rangos = list(range(0, max(longitudes) + 51, 50))

    plt.figure(figsize=(8, 5))
    plt.hist(longitudes, bins=rangos, color="orange", edgecolor="black")
    plt.title("Distribución de la longitud de las líneas")
    plt.xlabel("Cantidad de caracteres por línea")
    plt.ylabel("Número de líneas")
    plt.xticks(rangos)
    guardar_grafico("grafico2_longitudes.png")


def menu_txt():
    ruta = input("Ruta del archivo .txt (ej. data/libro.txt): ").strip()
    if not ruta.endswith(".txt"):
        print("El archivo debe tener extensión .txt")
        return

    lineas = leer_lineas(ruta)
    if len(lineas) == 0:
        print("No hay líneas para analizar.")
        return

    opcion = 0
    while opcion != 5:
        print(" PROCESAMIENTO DE TEXTOS ")
        print("1. Resumen estadístico")
        print("2. Extraer patrones (logs)")
        print("3. Gráfico: top 10 palabras")
        print("4. Gráfico: longitud de líneas")
        print("5. Volver")
        opcion = pedir_numero("Opción: ", 1, 5)

        if opcion == 1:
            resumen_texto(lineas)
        elif opcion == 2:
            extraer_patrones(lineas)
        elif opcion == 3:
            grafico_palabras(lineas)
        elif opcion == 4:
            grafico_longitudes(lineas)