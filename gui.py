import customtkinter as ctk
import subprocess
import sys
from backend import *
from lib_installer import *


def center_app(window, width: int, height: int):
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
        self.geometry("560x320")
        self.title("Recording script to .rpp file")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        # Widgets
        self.frame = MyFrame(master=self, )
        self.frame.grid(padx=6, pady=6, sticky="nsew")



class MyFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=0)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        # ROW 0
        self.label_script = ctk.CTkLabel(master=self, text="Enter script file path: ", fg_color="transparent")
        self.label_script.grid(row=0, column=0, padx=10, pady=(25, 10), sticky="nsew")

        self.entry_script = ctk.CTkEntry(master=self, placeholder_text="Type or paste file path", width=370)
        self.entry_script.grid(row=0, column=1, padx=10, pady=(25, 10))
        self.entry_script.bind("<KeyRelease>", lambda event: self.check_entries())

        # ROW 1
        self.label_audio_path = ctk.CTkLabel(master=self, text="Enter audio file location: ", fg_color="transparent")
        self.label_audio_path.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.entry_audio_path = ctk.CTkEntry(master=self, placeholder_text="Type or paste directory path", width=370)
        self.entry_audio_path.grid(row=1, column=1, padx=10, pady=10, )
        self.entry_audio_path.bind("<KeyRelease>", lambda event: self.check_entries())

        # ROW 2
        self.label_samplerate = ctk.CTkLabel(master=self, text="Sample rate: ", fg_color="transparent")
        self.label_samplerate.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.box_samplerate = ctk.CTkComboBox(master=self, values=["44100", "48000", "96000",], state="readonly")
        self.box_samplerate.grid(row=2, column=1, padx=(0, 230), pady=(10, 10))
        self.box_samplerate.bind("<KeyRelease>", lambda event: self.check_entries())

        # ROW 3
        self.label_excel_column_1 = ctk.CTkLabel(master=self, text="Filename column: ", fg_color="transparent")
        self.label_excel_column_1.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        self.entry_excel_column_1 = ctk.CTkEntry(master=self, placeholder_text="Column name here", width=370)
        self.entry_excel_column_1.grid(row=3, column=1, padx=10, pady=10, )
        self.entry_excel_column_1.bind("<KeyRelease>", lambda event: self.check_entries())

        # ROW 4
        self.label_excel_column_2 = ctk.CTkLabel(master=self, text="Item notes column: ", fg_color="transparent")
        self.label_excel_column_2.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)

        self.entry_excel_column_2 = ctk.CTkEntry(master=self, placeholder_text="Column name here", width=370)
        self.entry_excel_column_2.grid(row=4, column=1, padx=10, pady=10, )
        self.entry_excel_column_2.bind("<KeyRelease>", lambda event: self.check_entries())

        # ROW 5
        self.label_result = ctk.CTkLabel(master=self, text=" ", fg_color="transparent",
                                         wraplength=200, width=250)
        self.label_result.grid(row=5, column=0, padx=(10,10), columnspan=2, sticky="w")

        self.button_continue = ctk.CTkButton(master=self, text="Generate", border_spacing=1, border_color="black",
                                             border_width=1, command=self.generate_results, state="disabled")
        self.button_continue.grid(row=5, column=1, padx=(0, 25), pady=(10,10),sticky="SE")


    # METHODS
    def check_entries(self):
        # Retrieve values from entry boxes
        script_path = self.entry_script.get()
        audio_path = self.entry_audio_path.get()
        sample_rate = self.box_samplerate.get()
        excel_column_1 = self.entry_excel_column_1.get()
        excel_column_2 = self.entry_excel_column_2.get()

        # Check if all entries are filled
        if script_path and audio_path and sample_rate and excel_column_1 and excel_column_2:
            self.button_continue.configure(state="normal")
        else:
            self.button_continue.configure(state="disabled")

    def generate_results(self):
        script_path = self.entry_script.get()
        audio_path = self.entry_audio_path.get()
        sample_rate = self.box_samplerate.get()
        excel_column_1 = self.entry_excel_column_1.get()
        excel_column_2 = self.entry_excel_column_2.get()

        if not validate_path(script_path):
            self.label_result.configure(text="Invalid script file path.")
            return

        if not validate_directory(audio_path):
            self.label_result.configure(text="Invalid audio file location.")
            return

        if not validate_sample_rate(sample_rate):
            self.label_result.configure(text="Invalid sample rate.")
            return

        if not validate_excel_column(excel_column_1, script_path):
            self.label_result.configure(text=f"Not in excel file headers.")
            return

        if not validate_excel_column(excel_column_2, script_path):
            self.label_result.configure(text=f"Not in excel file headers.")
            return



        result = process_data(script_path.strip('"'), audio_path.strip('"'), sample_rate, excel_column_1, excel_column_2)
        self.label_result.configure(text=result)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
ctk.set_widget_scaling(True)
ctk.set_window_scaling(True)

install_requirements_in_directory("C:/Apps/Rec_script_to_Rpp")
app = App()
center_app(app, 560, 320)
app.mainloop()
