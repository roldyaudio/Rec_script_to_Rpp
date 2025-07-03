import customtkinter as ctk
import subprocess
import sys

# Package installation
def install_requirements():
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                                capture_output=True, text=True)

        if result.returncode == 0:
            print("Dependencies installed successfully.")
            if "Requirement already satisfied" in result.stdout:
                print("Some packages were already installed.")
        else:
            print(f"Error installing dependencies: {result.stderr}")
            sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


def center_hub(window, width: int, height: int):
    """Centers the window to the main display/monitor"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Configure
        self.title("App hub Launcher")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)







install_requirements()
app = App()
center_hub(app, 280, 320)
app.mainloop()