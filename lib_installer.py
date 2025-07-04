import os
import subprocess
import sys

def ensure_pip():
    try:
        import pip
        print("✅ pip ya está instalado.")
    except ImportError:
        print("⚠️ pip no encontrado. Instalando con ensurepip...")
        subprocess.check_call([sys.executable, "-m", "ensurepip"])
        print("✅ pip instalado correctamente.")

def install_requirements_in_current_directory():
    req_path = os.path.join(os.getcwd(), "requirements.txt")
    if os.path.isfile(req_path):
        print(f"🔍 Encontrado {req_path}. Instalando dependencias...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", req_path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("✅ Dependencias instaladas correctamente.")
            if "Requirement already satisfied" in result.stdout:
                print("ℹ️ Algunos paquetes ya estaban instalados.")
        else:
            print(f"❌ Error instalando dependencias: {result.stderr}")
            sys.exit(1)
    else:
        print("🚫 No se encontró requirements.txt en esta carpeta.")

if __name__ == "__main__":
    print("🔧 Verificando pip...")
    ensure_pip()
    print("🚀 Procesando requirements.txt en carpeta actual...")
    install_requirements_in_current_directory()
    print("✅ Proceso finalizado.")