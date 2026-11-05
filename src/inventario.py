import json
import csv
import yaml
import requests
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"


def cargar_json():
    with open(DATA_DIR / "inventario.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def cargar_csv():
    dispositivos = []

    with open(DATA_DIR / "inventario.csv", "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            dispositivos.append(fila)

    return dispositivos


def cargar_yaml():
    with open(DATA_DIR / "inventario.yaml", "r", encoding="utf-8") as archivo:
        datos = yaml.safe_load(archivo)

    return datos["dispositivos"]


def analizar_inventario(dispositivos):
    total = len(dispositivos)
    activos = 0
    mantenimiento = 0

    for dispositivo in dispositivos:
        if dispositivo["estado"] == "Activo":
            activos += 1
        elif dispositivo["estado"] == "Mantenimiento":
            mantenimiento += 1

    return {
        "total_dispositivos": total,
        "dispositivos_activos": activos,
        "dispositivos_mantenimiento": mantenimiento
    }


def consultar_api():
    url = "https://jsonplaceholder.typicode.com/posts"

    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()

        datos = respuesta.json()

        return {
            "conexion": "exitosa",
            "codigo_http": respuesta.status_code,
            "registros_recibidos": len(datos)
        }

    except requests.exceptions.Timeout:
        return {
            "conexion": "error",
            "mensaje": "Tiempo de espera agotado"
        }

    except requests.exceptions.HTTPError as error:
        return {
            "conexion": "error",
            "mensaje": f"Error HTTP: {error}"
        }

    except requests.exceptions.RequestException as error:
        return {
            "conexion": "error",
            "mensaje": f"Error de conexión: {error}"
        }


def generar_reporte():
    inventario_json = cargar_json()
    inventario_csv = cargar_csv()
    inventario_yaml = cargar_yaml()

    analisis = analizar_inventario(inventario_json)
    api = consultar_api()

    reporte = {
        "proyecto": "Automatización de inventario de dispositivos de red",
        "fuentes": {
            "json": len(inventario_json),
            "csv": len(inventario_csv),
            "yaml": len(inventario_yaml)
        },
        "analisis": analisis,
        "rest_api_https": api
    }

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(
        OUTPUT_DIR / "reporte_inventario.json",
        "w",
        encoding="utf-8"
    ) as archivo:
        json.dump(reporte, archivo, indent=4, ensure_ascii=False)

    print("==========================================")
    print(" SISTEMA DE AUTOMATIZACIÓN DE INVENTARIO")
    print("==========================================")
    print(f"Total de dispositivos: {analisis['total_dispositivos']}")
    print(f"Dispositivos activos: {analisis['dispositivos_activos']}")
    print(f"En mantenimiento: {analisis['dispositivos_mantenimiento']}")
    print("------------------------------------------")
    print(f"API HTTPS: {api}")
    print("------------------------------------------")
    print("Reporte generado correctamente.")
    print("Archivo: output/reporte_inventario.json")


if __name__ == "__main__":
    generar_reporte()
