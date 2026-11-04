import csv
import matplotlib.pyplot as plt
from utilidades import pedir_numero, obtener_cantidad, guardar_grafico


def leer_csv(ruta):
    """Devuelve (encabezados, datos). Si algo falla, devuelve listas vacías."""
    try:
        with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
            filas = list(csv.reader(archivo))
    except FileNotFoundError:
        print("Error: no se encontró el archivo.")
        return [], []
    except UnicodeDecodeError:
        print("Error: el archivo no está en formato UTF-8.")
        return [], []

    if len(filas) < 2:
        print("El archivo no tiene suficientes datos.")
        return [], []

    datos = []
    for fila in filas[1:]:
        if len(fila) > 0:
            datos.append(fila)
    return filas[0], datos


def elegir_columna(encabezados, mensaje):
    print("\nColumnas disponibles:")
    for i in range(len(encabezados)):
        print(f"  {i + 1}. {encabezados[i]}")
    numero = pedir_numero(mensaje, 1, len(encabezados))
    return numero - 1


def convertir_numero(texto):
    """Convierte un texto a float. Si no se puede (vacío o letras), devuelve None."""
    try:
        return float(texto)
    except ValueError:
        return None


def obtener_numeros(datos, indice):
    numeros = []
    for fila in datos:
        if indice < len(fila):
            valor = convertir_numero(fila[indice])
            if valor is not None:
                numeros.append(valor)
    return numeros


def obtener_pares(datos, i_x, i_y, x_es_numero):
    """Devuelve dos listas (x, y) solo con las filas donde ambos valores son válidos."""
    lista_x = []
    lista_y = []
    for fila in datos:
        if i_x < len(fila) and i_y < len(fila):
            y = convertir_numero(fila[i_y])
            if x_es_numero:
                x = convertir_numero(fila[i_x])
            else:
                x = fila[i_x].strip()
            if x is not None and x != "" and y is not None:
                lista_x.append(x)
                lista_y.append(y)
    return lista_x, lista_y


def calcular_mediana(numeros):
    ordenados = sorted(numeros)
    n = len(ordenados)
    mitad = n // 2
    if n % 2 == 0:
        return (ordenados[mitad - 1] + ordenados[mitad]) / 2
    return ordenados[mitad]


def vista_previa(encabezados, datos):
    print("\n" + " | ".join(encabezados))
    print("--- Primeras 10 filas ---")
    for fila in datos[:10]:
        print(" | ".join(fila))
    print("--- Últimas 5 filas ---")
    for fila in datos[-5:]:
        print(" | ".join(fila))
    print(f"Total de filas: {len(datos)}")


def estadisticas(encabezados, datos):
    indice = elegir_columna(encabezados, "Elija una columna numérica: ")
    numeros = obtener_numeros(datos, indice)
    if len(numeros) == 0:
        print("Esa columna no tiene valores numéricos.")
        return

    print(f"\nEstadísticas de '{encabezados[indice]}':")
    print(f"  Registros válidos: {len(numeros)} (descartados: {len(datos) - len(numeros)})")
    print(f"  Promedio: {sum(numeros) / len(numeros):.2f}")
    print(f"  Mediana: {calcular_mediana(numeros):.2f}")
    print(f"  Máximo: {max(numeros)}")
    print(f"  Mínimo: {min(numeros)}")


def grafico_tendencia(encabezados, datos):
    i_x = elegir_columna(encabezados, "Columna para el eje X (ej. mes): ")
    i_y = elegir_columna(encabezados, "Columna numérica para el eje Y: ")
    etiquetas, valores = obtener_pares(datos, i_x, i_y, False)
    if len(valores) == 0:
        print("No hay datos numéricos válidos para graficar.")
        return

    totales = {}
    for i in range(len(etiquetas)):
        etiqueta = etiquetas[i]
        totales[etiqueta] = totales.get(etiqueta, 0) + valores[i]

    nombres = list(totales.keys())
    sumas = list(totales.values())

    plt.figure(figsize=(10, 5))
    plt.plot(nombres, sumas, marker="o", color="green")
    plt.xticks(rotation=45)
    plt.title(f"Total de {encabezados[i_y]} por {encabezados[i_x]}")
    plt.xlabel(encabezados[i_x])
    plt.ylabel(f"Total de {encabezados[i_y]}")
    plt.grid(True)
    guardar_grafico("grafico3_tendencia.png")


def grafico_categorias(encabezados, datos):
    indice = elegir_columna(encabezados, "Elija una columna categórica: ")
    conteo = {}
    for fila in datos:
        if indice < len(fila) and fila[indice].strip() != "":
            categoria = fila[indice].strip()
            conteo[categoria] = conteo.get(categoria, 0) + 1

    ordenadas = sorted(conteo.items(), key=obtener_cantidad, reverse=True)
    etiquetas = []
    valores = []
    for categoria, cantidad in ordenadas[:6]:
        etiquetas.append(categoria)
        valores.append(cantidad)

    otros = 0
    for categoria, cantidad in ordenadas[6:]:
        otros += cantidad
    if otros > 0:
        etiquetas.append("Otros")
        valores.append(otros)

    plt.figure(figsize=(7, 7))
    plt.pie(valores, labels=etiquetas, autopct="%1.1f%%", startangle=90)
    plt.title(f"Participación por {encabezados[indice]}")
    plt.axis("equal")
    guardar_grafico("grafico4_categorias.png")


def grafico_dispersion(encabezados, datos):
    i_x = elegir_columna(encabezados, "Primera columna numérica (eje X): ")
    i_y = elegir_columna(encabezados, "Segunda columna numérica (eje Y): ")
    lista_x, lista_y = obtener_pares(datos, i_x, i_y, True)
    if len(lista_x) == 0:
        print("No hay pares numéricos válidos.")
        return

    plt.figure(figsize=(8, 5))
    plt.scatter(lista_x, lista_y, color="purple", alpha=0.6)
    plt.title(f"Relación entre {encabezados[i_x]} y {encabezados[i_y]}")
    plt.xlabel(encabezados[i_x])
    plt.ylabel(encabezados[i_y])
    plt.grid(True)
    guardar_grafico("grafico5_dispersion.png")


def menu_csv():
    ruta = input("Ruta del archivo .csv (ej. data/clima.csv): ").strip()
    if not ruta.endswith(".csv"):
        print("El archivo debe tener extensión .csv")
        return

    encabezados, datos = leer_csv(ruta)
    if len(datos) == 0:
        return

    opcion = 0
    while opcion != 6:
        print(" ANÁLISIS DE DATASET ")
        print("1. Vista previa")
        print("2. Estadísticas descriptivas")
        print("3. Gráfico de tendencia (líneas)")
        print("4. Gráfico de categorías (pastel)")
        print("5. Gráfico de correlación (dispersión)")
        print("6. Volver")
        opcion = pedir_numero("Opción: ", 1, 6)

        if opcion == 1:
            vista_previa(encabezados, datos)
        elif opcion == 2:
            estadisticas(encabezados, datos)
        elif opcion == 3:
            grafico_tendencia(encabezados, datos)
        elif opcion == 4:
            grafico_categorias(encabezados, datos)
        elif opcion == 5:
            grafico_dispersion(encabezados, datos)