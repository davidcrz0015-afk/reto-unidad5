import os
import matplotlib.pyplot as plt

CARPETA_SALIDA = "outputs"


def pedir_numero(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"Debe ser un número entre {minimo} y {maximo}.")
        except ValueError:
            print("Debe escribir un número entero.")


def obtener_cantidad(par):
    return par[1]


def guardar_grafico(nombre_archivo):
    """Guarda el gráfico actual en la carpeta outputs y lo muestra."""
    ruta = os.path.join(CARPETA_SALIDA, nombre_archivo)
    plt.tight_layout()
    plt.savefig(ruta)
    print(f"Gráfico guardado en: {ruta}")
    plt.show()
    plt.close()