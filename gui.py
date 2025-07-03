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
    x = int((screen_width / 2) - (width / -2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Configure
        self.title("Recording script to .rpp file")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=0)

        self.frame = MyFrame(master=self, )
        self.frame.grid(padx=6, pady=6, sticky="nsew")


class MyFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=0)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        # ROW 0
        self.label_script = ctk.CTkLabel(master=self, text="Enter script file path: ",
                                         fg_color="transparent")
        self.label_script.grid(row=0, column=0, padx=10, pady=10, sticky="W")

        self.entry_script = ctk.CTkEntry(master=self,
                                         placeholder_text="Type or paste file path",
                                         width=370)
        self.entry_script.grid(row=0, column=1, padx=10, pady=10)

        # ROW 1
        self.label_audio_path = ctk.CTkLabel(master=self, text="Enter audio file location: ",
                                         fg_color="transparent")
        self.label_audio_path.grid(row=1, column=0, padx=10, pady=10, sticky="W")
        self.entry_audio_path = ctk.CTkEntry(master=self,
                                         placeholder_text="Type or paste directory path",
                                         width=370)
        self.entry_audio_path.grid(row=1, column=1, padx=10, pady=10, )

        self.label_excel_column_1 = ctk.CTkLabel(master=self, text="Filename column: ",
                                         fg_color="transparent")
        self.label_excel_column_1.grid(row=3, column=0, sticky="W", padx=10, pady=10)
        self.entry_excel_column_1 = ctk.CTkEntry(master=self,
                                             placeholder_text="Column name here",
                                             width=370)
        self.entry_excel_column_1.grid(row=3, column=1, padx=10, pady=10, )

        self.label_excel_column_2 = ctk.CTkLabel(master=self, text="Item notes column: ",
                                                 fg_color="transparent")
        self.label_excel_column_2.grid(row=4, column=0, sticky="W", padx=10, pady=10)
        self.entry_excel_column_2 = ctk.CTkEntry(master=self,
                                                 placeholder_text="Column name here",
                                                 width=370)
        self.entry_excel_column_2.grid(row=4, column=1, padx=10, pady=10, )


        self.label_samplerate = ctk.CTkLabel(master=self, text="Sample rate: ",
                                             fg_color="transparent")
        self.label_samplerate.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.box_samplerate = ctk.CTkComboBox(master=self, values=["44100", "48000", "96000"])
        self.box_samplerate.grid(row=2, column=1, padx=(0, 230), pady=(10, 10))

        self.button_continue = ctk.CTkButton(master=self, text="Generate",
                                               border_spacing=1, border_color="black",
                                             border_width=1)
        self.button_continue.grid(row=5, column=1, padx=(25, 25), pady=(10,10),sticky="SE")

        self.label_result = ctk.CTkLabel(master=self, text="Results will be shown here",
                                                 fg_color="transparent")
        self.label_result.grid(row=5, column=0, sticky="W", padx=(20,20))


install_requirements()
app = App()
center_hub(app, 584, 320)
app.mainloop()
