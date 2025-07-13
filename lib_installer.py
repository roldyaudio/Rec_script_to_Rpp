import os
import subprocess
import sys
import time
import pkg_resources


def ensure_pip():
    try:
        import pip
        print("✅ pip is already installed.")
    except ImportError:
        print("⚠️ pip not found. Installing with ensurepip...")
        subprocess.check_call([sys.executable, "-m", "ensurepip"])
        print("✅ pip installed successfully.")


def install_requirements_in_directory(base_dir):
    """
    Walk through all folders inside base_dir looking for requirements.txt files.
    For each requirement:
    - If already installed with the correct version, skips it.
    - If not installed, installs it.
    - If installed but with different version, warns and skips.
    """
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == "requirements.txt":
                req_path = os.path.join(root, file)
                print(f"\n🔍 Found requirements: {req_path}")

                # Read the requirements
                with open(req_path, 'r') as f:
                    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

                for req in requirements:
                    try:
                        pkg_resources.require(req)
                        print(f"✅ {req} is already installed with the correct version.")
                    except pkg_resources.DistributionNotFound:
                        print(f"📦 {req} is not installed. Installing...")
                        result = subprocess.run([sys.executable, "-m", "pip", "install", req])
                        if result.returncode == 0:
                            print(f"✅ Successfully installed {req}")
                        else:
                            print(f"❌ Failed to install {req}")
                            sys.exit(1)
                    except pkg_resources.VersionConflict as e:
                        installed = e.dist.version
                        expected = e.req
                        print(f"⚠ Version conflict for {req}: installed {installed}, expected {expected}. Skipping installation of this package.")


if __name__ == "__main__":
    # if sys.version_info >= (3, 13):
    #     print("❌ This script requires Python 3.12 or lower, because pydub needs audioop.")
    #     time.sleep(5)
    #     sys.exit(1)

    print("🔧 Checking pip...")
    ensure_pip()
    print("🚀 Processing requirements.txt in current folder...")
    install_requirements_in_directory("C:/Apps/Rec_script_to_Rpp")
    print("✅ Process completed.")
