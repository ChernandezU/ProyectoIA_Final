"""
Script de Instalación Automática
Configura el entorno completo del proyecto
"""
import os
import sys
import subprocess
from pathlib import Path


def run_command(cmd, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n▶️  {description}")
    print(f"   Comando: {cmd}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completado")
            return True
        else:
            print(f"❌ Error en: {description}")
            return False
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False


def setup_venv():
    """Crea el entorno virtual"""
    print("\n" + "=" * 70)
    print("1️⃣  Creando Entorno Virtual")
    print("=" * 70)
    
    if Path("venv").exists():
        print("✅ Entorno virtual ya existe")
        return True
    
    return run_command("python -m venv venv", "Crear entorno virtual")


def install_dependencies():
    """Instala las dependencias"""
    print("\n" + "=" * 70)
    print("2️⃣  Instalando Dependencias")
    print("=" * 70)
    
    if sys.platform == "win32":
        activate_cmd = ".\\venv\\Scripts\\activate && "
    else:
        activate_cmd = "source venv/bin/activate && "
    
    cmd = activate_cmd + "pip install -r requirements.txt"
    return run_command(cmd, "Instalar paquetes Python")


def verify_data_files():
    """Verifica que los archivos de datos existan"""
    print("\n" + "=" * 70)
    print("3️⃣  Verificando Archivos de Datos")
    print("=" * 70)
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    required_files = [
        "data/archivo1_documentos.json",
        "data/archivo2_grafo.csv",
        "data/archivo3_acciones.json"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"⚠️  {file_path} (falta crear)")
            all_exist = False
    
    return all_exist


def create_env_file():
    """Crea archivo .env si no existe"""
    print("\n" + "=" * 70)
    print("4️⃣  Configurando Variables de Entorno")
    print("=" * 70)
    
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Archivo .env ya existe")
        return True
    
    # Copiar desde .env.example si existe
    env_example = Path(".env.example")
    if env_example.exists():
        with open(env_example, 'r') as f:
            content = f.read()
        with open(env_file, 'w') as f:
            f.write(content)
        print("✅ Archivo .env creado desde .env.example")
        return True
    
    print("⚠️  Archivo .env.example no encontrado")
    return False


def run_tests():
    """Ejecuta pruebas básicas"""
    print("\n" + "=" * 70)
    print("5️⃣  Ejecutando Pruebas")
    print("=" * 70)
    
    if sys.platform == "win32":
        activate_cmd = ".\\venv\\Scripts\\activate && "
    else:
        activate_cmd = "source venv/bin/activate && "
    
    cmd = activate_cmd + "python test_data.py"
    return run_command(cmd, "Ejecutar test_data.py")


def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print("🚀 Instalador Automático - HernandezCristian_ProyectoIA")
    print("=" * 70)
    
    steps = [
        ("Crear Entorno Virtual", setup_venv),
        ("Instalar Dependencias", install_dependencies),
        ("Verificar Archivos", verify_data_files),
        ("Configurar Variables", create_env_file),
        ("Ejecutar Pruebas", run_tests),
    ]
    
    completed = 0
    for step_name, step_func in steps:
        try:
            if step_func():
                completed += 1
            else:
                print(f"⚠️  Paso '{step_name}' falló pero continuando...")
        except Exception as e:
            print(f"❌ Error en '{step_name}': {e}")
    
    print("\n" + "=" * 70)
    print("✅ Instalación Completada")
    print("=" * 70)
    
    print(f"\n📊 Pasos completados: {completed}/{len(steps)}")
    
    print("\n📝 Próximos pasos:")
    print(f"   1. Activar entorno virtual:")
    if sys.platform == "win32":
        print(f"      .\\venv\\Scripts\\activate")
    else:
        print(f"      source venv/bin/activate")
    
    print(f"\n   2. Ejecutar el servidor:")
    print(f"      python run.py")
    
    print(f"\n   3. Editar configuración (si es necesario):")
    print(f"      - Archivo: .env")
    print(f"      - Añadir credenciales de Neo4j Aura si lo deseas")


if __name__ == "__main__":
    main()
