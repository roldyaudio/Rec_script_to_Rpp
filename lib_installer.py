import os
import subprocess
import sys
import importlib.metadata

def ensure_pip():
    """Ensures pip is available without importing it directly (which can be unstable)."""
    try:
        # Check if pip is reachable as a module
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                       check=True, capture_output=True)
        print("✅ pip is already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ pip not found. Installing via ensurepip...")
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
        print("✅ pip installed successfully.")

def is_installed(req_string):
    """
    Checks if a package and its version requirements are met.
    Replaces the deprecated pkg_resources.
    """
    try:
        # We use the 'packaging' library to parse complex version specs (e.g. >=2.0)
        from packaging.requirements import Requirement
        from packaging.version import parse as parse_version
    except ImportError:
        # Bootstrapping 'packaging' if missing
        print("📦 Installing helper dependency 'packaging'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "packaging"])
        from packaging.requirements import Requirement

    try:
        req = Requirement(req_string)
        # Get version of the installed distribution
        dist_version = importlib.metadata.version(req.name)
        
        # If no specific version is required, just checking existence is enough
        if not req.specifier:
            return True, dist_version
        
        # Validate if the installed version matches the specifiers (e.g., == or >=)
        if dist_version in req.specifier:
            return True, dist_version
        else:
            return False, dist_version
            
    except importlib.metadata.PackageNotFoundError:
        return False, None
    except Exception as e:
        print(f"❌ Error parsing {req_string}: {e}")
        return False, None

def install_requirements_in_directory(base_dir):
    """
    Walks through base_dir to find requirements.txt files and manages installation.
    """
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file == "requirements.txt":
                req_path = os.path.join(root, file)
                print(f"\n🔍 Processing: {req_path}")

                try:
                    with open(req_path, 'r', encoding='utf-8') as f:
                        # Filter out empty lines and comments
                        requirements = [line.strip() for line in f 
                                       if line.strip() and not line.startswith(('#', '-r'))]
                except Exception as e:
                    print(f"❌ Could not read {req_path}: {e}")
                    continue

                for req in requirements:
                    installed, current_v = is_installed(req)
                    
                    if installed:
                        print(f"✅ {req} is already satisfied (Installed: {current_v}).")
                    elif current_v:
                        # Version exists but doesn't match requirement
                        print(f"⚠️ Conflict: {req} requested, but version {current_v} is currently installed. Skipping to prevent breaking environment.")
                    else:
                        # Package not found at all
                        print(f"📦 {req} not found. Installing...")
                        result = subprocess.run([sys.executable, "-m", "pip", "install", req])
                        if result.returncode == 0:
                            print(f"✅ Successfully installed {req}")
                        else:
                            print(f"❌ Failed to install {req}")
                            sys.exit(1)

if __name__ == "__main__":
    # Note: Python 3.13+ removed 'audioop'. 
    # If your project relies on 'pydub', ensure you are running on Python 3.12 or lower.
    
    print("🔧 Checking environment...")
    ensure_pip()
    
    # Target directory
    BASE_PATH = r"C:/Apps/Rec_script_to_Rpp"
    
    if os.path.exists(BASE_PATH):
        install_requirements_in_directory(BASE_PATH)
        print("\n✅ Setup process completed.")
    else:
        print(f"❌ The path {BASE_PATH} does not exist. Please check the directory.")
