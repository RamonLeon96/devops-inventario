import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from inventario import analizar_inventario


def test_analizar_inventario():
    dispositivos = [
        {
            "id": 1,
            "hostname": "R1-Piura",
            "ip": "192.168.10.1",
            "tipo": "Router",
            "estado": "Activo"
        },
        {
            "id": 2,
            "hostname": "SW1-Piura",
            "ip": "192.168.10.10",
            "tipo": "Switch",
            "estado": "Activo"
        },
        {
            "id": 3,
            "hostname": "AP1-Piura",
            "ip": "192.168.10.20",
            "tipo": "Access Point",
            "estado": "Mantenimiento"
        }
    ]

    resultado = analizar_inventario(dispositivos)

    assert resultado["total_dispositivos"] == 3
    assert resultado["dispositivos_activos"] == 2
    assert resultado["dispositivos_mantenimiento"] == 1


if __name__ == "__main__":
    test_analizar_inventario()
    print("Prueba ejecutada correctamente.")
