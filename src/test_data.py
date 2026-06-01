import json
import csv
import os

# Detectar automáticamente la raíz del proyecto (un nivel arriba de 'src')
RUTA_DEL_SCRIPT = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROYECTO = os.path.dirname(RUTA_DEL_SCRIPT)
CARPETA_DATA = os.path.join(RAIZ_PROYECTO, "data")

print("============================================================")
print("TEST DATA - Validación de archivos")
print("============================================================")
print(f"📁 Buscando carpeta 'data' en: {CARPETA_DATA}\n")

if not os.path.exists(CARPETA_DATA):
    print("❌ La carpeta 'data' NO existe en la raíz del proyecto.")
    print("💡 Solución: Crea una carpeta llamada 'data' en la raíz de tu proyecto (afuera de 'src').")
else:
    print("✅ Carpeta 'data' encontrada. Verificando archivos internos...\n")
    
    # 1. Probar lectura de archivo1_documentos.json
    path_json1 = os.path.join(CARPETA_DATA, "archivo1_documentos.json")
    if os.path.exists(path_json1):
        with open(path_json1, "r", encoding="utf-8") as f:
            data_docs = json.load(f)
        print(f"✅ 'archivo1_documentos.json' leído correctamente. ({len(data_docs)} documentos).")
    else:
        print("❌ No se encontró 'archivo1_documentos.json' dentro de la carpeta data.")

    # 2. Probar lectura de archivo2_grafo.csv
    path_csv = os.path.join(CARPETA_DATA, "archivo2_grafo.csv")
    if os.path.exists(path_csv):
        with open(path_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)  # Saltar cabecera
            filas = list(reader)
        print(f"✅ 'archivo2_grafo.csv' leído correctamente. ({len(filas)} relaciones).")
    else:
        print("❌ No se encontró 'archivo2_grafo.csv' dentro de la carpeta data.")

    # 3. Probar lectura de archivo3_acciones.json
    path_json3 = os.path.join(CARPETA_DATA, "archivo3_acciones.json")
    if os.path.exists(path_json3):
        with open(path_json3, "r", encoding="utf-8") as f:
            data_acciones = json.load(f)
        print(f"✅ 'archivo3_acciones.json' leído correctamente. ({len(data_acciones)} acciones).")
    else:
        print("❌ No se encontró 'archivo3_acciones.json' dentro de la carpeta data.")