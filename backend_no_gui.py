from pydub import AudioSegment
import pandas as pd
import os
from pathlib import Path
import concurrent
from uuid import uuid4
from random import randint
from concurrent.futures import ThreadPoolExecutor


# Functions for Dataframe
def get_rec_script_path():
    """Returns the path to the file with the recording script"""
    while True:
        # Prompt user for input
        file_path = input("Please enter the path to your Recording Script file: ").strip()
        # Remove surrounding quotes if present
        if (file_path.startswith('"') and file_path.endswith('"')) or (
                file_path.startswith("'") and file_path.endswith("'")):
            file_path = file_path[1:-1]
        # Check if the file path is valid
        if os.path.isfile(file_path):
            # print(file_path)
            return file_path
        else:
            print("The path you entered is not valid or the file does not exist. Please try again... ")


def get_directory_path(path_to_where):
    """Returns the path to the directory containing whatever you are pointing to"""

    # Prompt user for input
    dir_path = input(f"Please enter the path leading to your {path_to_where}: ").strip()
    # Remove surrounding quotes if present
    if (dir_path.startswith('"') and dir_path.endswith('"')) or (dir_path.startswith("'") and dir_path.endswith("'")):
        dir_path = dir_path[1:-1]
    # Check if the directory path is valid
    if os.path.isdir(dir_path):
        return dir_path
    else:
        print("The path you entered is not valid or the directory does not exist. Please try again.")
        return None


def get_wav_file_paths_list(directory_path):
    """Returns a list with full wav file paths contained in a directory and its subdirectories"""
    wav_file_paths = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.wav'):
                wav_file_paths.append(os.path.join(root, file))
    return wav_file_paths


def export_dataframe_to_excel_file(df, filename, directory):
    """Exports the given DataFrame to an Excel file in the specified directory."""
    # Ensure filename ends with .xlsx
    if not filename.lower().endswith('.xlsx'):
        filename += '.xlsx'

    file_path = os.path.join(directory, filename)
    df.to_excel(file_path, index=False, engine='openpyxl')


def new_frame_with_audio_paths(excel_file, list_of_columns, directory_path):
    # Detect file extension
    ext = os.path.splitext(excel_file)[1].lower()

    # Read the file based on extension
    if ext == '.xlsx':
        df = pd.read_excel(excel_file, engine='openpyxl')
    elif ext == '.xls':
        df = pd.read_excel(excel_file, engine='xlrd')
    elif ext == '.csv':
        df = pd.read_csv(excel_file)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    # Filter DataFrame with only specified columns
    df = df[list_of_columns]

    # print("Checkpoint 1")

    # Get list of wav file paths
    wav_file_paths = get_wav_file_paths_list(directory_path)

    # print("Checkpoint 2")

    # Map filenames to paths
    filename_to_path = {os.path.basename(path): path for path in wav_file_paths if path is not None}

    # print("Checkpoint 3")

    # Add audio path column, defaulting to None if not found
    df['Audio Path'] = df.iloc[:, 0].apply(lambda x: filename_to_path.get(x, None))

    # print("Checkpoint 4")

    # Add length column, defaulting to None if path is None
    # df['Length'] = df['Audio Path'].apply(lambda path: get_length(path) if path else None)

    # print("Checkpoint 5")

    # Add length column, defaulting to None if path is None

    with ThreadPoolExecutor() as executor:
        df['Length'] = list(executor.map(lambda path: get_length(path) if path else None, df['Audio Path']))

    # print("Checkpoint 6")

    # Add position column, defaulting to None if length is None
    df = assign_positions(df, length_column='Length', separation=4)

    # Handle missing values gracefully
    df['Audio Path'] = df['Audio Path'].fillna('Not Found')
    df['Length'] = df['Length'].fillna('Not Generated')
    df['Position'] = df['Position'].fillna('Not Assigned')

    return df


def get_length(file_path):
    audio = AudioSegment.from_file(file_path)
    length = audio.duration_seconds
    return length


def assign_positions(df, length_column='Length', separation=4):
    # Initialize position tracker
    current_position = 5

    # Create a list to store positions
    positions = []

    for index, row in df.iterrows():
        length = row[length_column]

        # If length is None, use a default value (e.g., 0)
        if length is None:
            length = 0

        # Calculate position
        positions.append(current_position)
        current_position += length + separation

    # Add positions to DataFrame
    df['Position'] = positions
    return df


def create_dataframe_for_rec():
    # get the rec script path and directory
    rec_script_path = get_rec_script_path()
    project_name = os.path.basename(rec_script_path).split(".")[0]
    rec_script_directory = os.path.dirname(rec_script_path)

    # audio location
    audios_location = ""

    # dataframe with filename and localized text
    df = pd.read_excel(rec_script_path)
    columns = df.columns.tolist()

    # User needed columns
    user_columns = []

    # New dataframe for item iteration

    dir_is_ok = False
    while not dir_is_ok:
        # get audio files directory
        audios_directory = get_directory_path("Audio files")
        if audios_directory is None or not os.path.isdir(audios_directory):
            continue
        else:
            audios_location = audios_directory
            dir_is_ok = True

    user_columns_are_ok = False
    while not user_columns_are_ok:
        # get filename and loc text headers
        column1_name = input("Enter the column name containing filenames: ")
        if column1_name not in columns:
            print(f"Header '{column1_name}' not in recording script")
            continue
        column2_name = input("Enter the column name containing item notes information: ")

        if column2_name not in columns:
            print(f"Header '{column2_name}' not in recording script")

        if column1_name not in columns or column2_name not in columns:
            print("Headers not found in file. Try again")
            continue

        else:
            user_columns.append(column1_name)
            user_columns.append(column2_name)
            user_columns_are_ok = True

    print("\nGenerating, please wait...\n")

    # start_time = time.time()

    # print("HASTA ACA")

    new_data = new_frame_with_audio_paths(rec_script_path, user_columns, audios_location)

    # print("HASTA ACA")

    project_dataframe = new_data

    # print("HASTA ACA")

    export_dataframe_to_excel_file(new_data, f"Dataframe_{os.path.basename(rec_script_path)}", rec_script_directory)

    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Elapsed time {elapsed_time} seconds")

    return [project_dataframe, rec_script_directory, project_name]


# Functions for Reaper project creation
def set_project_samplerate():
    """Ask the user for the Sample rate to use"""

    valid_options = ["44100", "48000", "96000"]
    while True:
        sample_rate = input("Input project sample rate: (44100, 48000, or 96000): ")
        if sample_rate in valid_options:
            return int(sample_rate)
        else:
            print("Invalid input. Please enter one of the specified rates.")


def generate_random_uuid():
    """Creates a unique random ID"""

    id1 = str(uuid4()).upper()
    return id1


def create_empty_project_template(sample_rate):
    """Create the structure of a Reaper project as text. Returns a string"""

    empty_template = f"""<REAPER_PROJECT 0.1 "7.39/win64" {randint(1747000000, 9999999999)}
  RIPPLE 0 0
  GROUPOVERRIDE 0 0 0
  AUTOXFADE 129
  ENVATTACH 0
  POOLEDENVATTACH 0
  MIXERUIFLAGS 11 48
  PEAKGAIN 1
  FEEDBACK 0
  PANLAW 1
  PROJOFFS 0 0 0
  MAXPROJLEN 0 600
  GRID 3198 8 1 8 1 0 0 0
  TIMEMODE 1 5 -1 30 0 0 -1
  VIDEO_CONFIG 0 0 256
  PANMODE 3
  CURSOR 0
  ZOOM 1
  VZOOMEX 5 0
  USE_REC_CFG 0
  RECMODE 1
  SMPTESYNC 0 30 100 40 1000 300 0 0 1 0 0
  MIDIEDITOR -10197916 0 0
  LOOP 0
  LOOPGRAN 0 4
  RECORD_PATH "" ""
  <RECORD_CFG
    ZXZhdxgBAA==
  >
  <APPLYFX_CFG
  >
  RENDER_FILE ""
  RENDER_PATTERN ""
  RENDER_FMT 0 1 48000
  RENDER_1X 0
  RENDER_RANGE 1 0 0 2 0
  RENDER_RESAMPLE 3 0 1
  RENDER_ADDTOPROJ 0
  RENDER_STEMS 6
  RENDER_DITHER 0
  RENDER_TRIM 0 0 0 0
  TIMELOCKMODE 1
  TEMPOENVLOCKMODE 1
  ITEMMIX 0
  DEFPITCHMODE 1 0
  TAKELANE 1
  SAMPLERATE {sample_rate} 1 0
  <RENDER_CFG
    ZXZhdxgDAA==
  >
  LOCK 1
  <METRONOME 6 2
    VOL 0.25 0.125
    BEATLEN 4
    FREQ 800 1600 1
    SAMPLES "" "" "" ""
    SPLIGNORE 0 0
    SPLDEF 2 660 "" 0 ""
    SPLDEF 3 440 "" 0 ""
    PATTERN 0 169
    PATTERNSTR ABBB
    MULT 1
  >
  GLOBAL_AUTO -1
  TEMPO 120 4 4 0
  PLAYRATE 1 0 0.25 4
  SELECTION 0 0
  SELECTION2 0 0
  MASTERAUTOMODE 0
  MASTERTRACKHEIGHT 0 0
  MASTERPEAKCOL 16576
  MASTERMUTESOLO 0
  MASTERTRACKVIEW 0 0.6667 0.5 0.5 0 0 0 0 0 0 0 0 0 0
  MASTERHWOUT 0 0 1 0 0 0 0 -1
  MASTER_NCH 2 2
  MASTER_VOLUME 1 0 -1 -1 1
  MASTER_PANMODE 3
  MASTER_FX 1
  MASTER_SEL 0
  <MASTERPLAYSPEEDENV
    EGUID {{{generate_random_uuid()}}}
    ACT 0 -1
    VIS 0 1 1
    LANEHEIGHT 0 0
    ARM 0
    DEFSHAPE 0 -1 -1
  >
  <TEMPOENVEX
    EGUID {{{generate_random_uuid()}}}
    ACT 1 -1
    VIS 1 0 1
    LANEHEIGHT 0 0
    ARM 0
    DEFSHAPE 1 -1 -1
  >
  <PROJBAY
  >
  <EXTENSIONS
  >
>"""
    return empty_template


def create_empty_track_template(track_name):
    """Create the structure of an empty track as text"""

    track_id = generate_random_uuid()

    empty_track_template = f"""<TRACK {{{track_id}}}
    NAME {track_name}
    PEAKCOL 16576
    BEAT -1
    AUTOMODE 0
    PANLAWFLAGS 3
    VOLPAN 1 0 -1 -1 1
    MUTESOLO 0 0 0
    IPHASE 0
    PLAYOFFS 0 1
    ISBUS 0 0
    BUSCOMP 0 0 0 0 0
    SHOWINMIX 1 0.6667 0.5 1 0.5 0 0 0
    FIXEDLANES 9 0 0 0 0
    SEL 0
    REC 0 0 0 0 0 0 0 0
    VU 2
    TRACKHEIGHT 0 0 0 0 0 0 0
    INQ 0 0 0 0.5 100 0 0 100
    NCHAN 2
    FX 1
    TRACKID {{{track_id}}}
    PERF 0
    MIDIOUT -1
    MAINSEND 1 0
>"""
    return empty_track_template


def create_item_template_with_notes(filename, file_path, text_notes, length, position):
    item_iguid = generate_random_uuid()
    item_guid = generate_random_uuid()

    item_template = f"""    <ITEM
      POSITION {position}
      SNAPOFFS 0
      LENGTH {length}
      LOOP 1
      ALLTAKES 0
      FADEIN 1 0 0 1 0 0 0
      FADEOUT 1 0 0 1 0 0 0
      MUTE 0 0
      SEL 0
      IGUID {{{item_iguid}}}
      IID 1
      <NOTES
        |{text_notes}
      >
      IMGRESOURCEFLAGS 0
      NOTESWND 544 398 1043 795
      NAME {filename}
      VOLPAN 1 0 1 -1
      SOFFS 0
      PLAYRATE 1 1 0 -1 0 0.0025
      CHANMODE 0
      GUID {{{item_guid}}}
      <SOURCE WAVE
        FILE "{file_path}"
      >
    >"""
    return item_template


def add_track_to_project(project, empty_track):
    insert_point = project.find("<EXTENSIONS\n  >")
    if insert_point != -1:
        # Insert the <TRACK> tag before <EXTENSIONS>
        project_template_with_track = (project[:insert_point] + empty_track + "\n  " + project[insert_point:])
        return project_template_with_track
    return None


def add_items_to_track(project_w_track, item_as_text):
    insert_point = project_w_track.find("MAINSEND 1 0\n")
    if insert_point != -1:
        # Insert the <TRACK> tag before <EXTENSIONS>
        insert_point += len("MAINSEND 1 0\n")
        project_template_with_track = (
                project_w_track[:insert_point] + item_as_text + "\n  " + project_w_track[insert_point:])
        return project_template_with_track
    return None


def generate_item_templates_from_dataframe(df):
    # Heuristic: first two string columns
    text_columns = df.select_dtypes(include='object').columns[:2]
    name_col, notes_col = text_columns

    templates = []

    def process_row(row):
        item_name = row[name_col]
        item_notes = row[notes_col]
        item_path = row['Audio Path']
        item_length = row['Length']
        item_position = row['Position']

        return create_item_template_with_notes(item_name, item_path, item_notes,
                                               item_length, item_position)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_row, row) for _, row in df.iterrows()]
        for future in concurrent.futures.as_completed(futures):
            templates.append(future.result())

    return "\n".join(templates)


# Functions to export .rpp file
def export_to_desktop(text, filename):
    """Save a text file to the user's Desktop."""
    desktop_path = Path.home() / "Desktop"
    full_path = desktop_path / filename
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return str(full_path)


def export_to_directory(text, filename, directory):
    """Save a text file to a specified directory."""
    dir_path = Path(directory)
    full_path = dir_path / filename
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return str(full_path)


# Execution
chosen_sample_rate = set_project_samplerate()
project_info = create_dataframe_for_rec()
empty_project = create_empty_project_template(chosen_sample_rate)
# print(empty_project)
new_track = create_empty_track_template("Source_Reference")
# print(new_track)
project_with_track = add_track_to_project(empty_project, new_track)
# print(project_with_track)
new_items_template = generate_item_templates_from_dataframe(project_info[0])
# print(new_items_template)
reaper_project_as_text = add_items_to_track(project_with_track, new_items_template)
# print(reaper_project_as_text)
export_to_directory(reaper_project_as_text, f"{project_info[2]}.rpp", project_info[1])
