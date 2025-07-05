import os
import subprocess
import sys
import time

def ensure_pip():
    try:
        import pip
        print("✅ pip ya está instalado.")
    except ImportError:
        print("⚠️ pip no encontrado. Instalando con ensurepip...")
        subprocess.check_call([sys.executable, "-m", "ensurepip"])
        print("✅ pip instalado correctamente.")



def install_requirements_in_directory(base_dir):
    # Recorre todas las carpetas buscando archivos requirements.txt
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == "requirements.txt":
                req_path = os.path.join(root, file)
                print(f"\nInstalando dependencias desde {req_path} ...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", req_path],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    print(f"✅ Instalado correctamente desde {req_path}")
                    if "Requirement already satisfied" in result.stdout:
                        print("   Algunos paquetes ya estaban instalados.")
                        time.sleep(5)
                else:
                    print(f"❌ Error instalando desde {req_path}: {result.stderr}")
                    sys.exit(1)
                    time.sleep(5)

if __name__ == "__main__":
    if sys.version_info >= (3, 13):
        print("❌ Este script requiere Python 3.12 o menor, porque pydub necesita audioop.")
        time.sleep(5)
        sys.exit(1)
        
    print("🔧 Verificando pip...")
    ensure_pip()
    print("🚀 Procesando requirements.txt en carpeta actual...")
    install_requirements_in_directory("C:/Apps")
    print("✅ Proceso finalizado.")