import os
import shutil
import zipfile
import py7zr
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

# Define the ROM extensions and their corresponding folders
rom_folders = {
    'nes': 'NES',  # Added .nes files to the NES folder
    'fds': 'NES',  # Added .fds files to the NES folder
    'smc': 'SNES',  # Added .smc files to the SNES folder
    'sfc': 'SNES',  # Added .sfc files to the SNES folder
    'fig': 'SNES',  # Added .fig files to the SNES folder
    'gb': 'Game Boy',  # Added .gb files to the Game Boy folder
    'gbc': 'Game Boy Color',  # Added .gbc files to the Game Boy Color folder
    'gba': 'Game Boy Advance',  # Added .gba files to the Game Boy Advance folder
    'i64': 'Nintendo 64',  # Added .i64 files to the Nintendo 64 folder
    'n64': 'Nintendo 64',  # Added .n64 files to the Nintendo 64 folder
    'v64': 'Nintendo 64',  # Added .v64 files to the Nintendo 64 folder
    'z64': 'Nintendo 64',  # Added .z64 files to the Nintendo 64 folder
    'nds': 'Nintendo DS',  # Added .nds files to the Nintendo DS folder
    'bin': 'Sega Genesis',  # Added .bin files to the Sega Genesis folder
    'gen': 'Sega Genesis',  # Added .gen files to the Sega Genesis folder
    'cdi': 'Sega Dreamcast',  # Added .cdi files to the Sega Dreamcast folder
    'gdi': 'Sega Dreamcast',  # Added .gdi files to the Sega Dreamcast folder
    'xci': 'Nintendo Switch',  # Added .xci files to the Nintendo Switch folder
    'nsp': 'Nintendo Switch'  # Added .nsp files to the Nintendo Switch folder
    
    # Not working yet, just added for future reference
    #'iso': 'Playstation',  # Added .iso files to the Playstation folder
    #'bin': 'Playstation',  # Added .bin files to the Playstation folder
    #'iso': 'Playstation 2',  # Added .iso files to the Playstation 2 folder
    #'bin': 'Playstation 2',  # Added .bin files to the Playstation 2 folder
    #'iso': 'Playstation Portable (PSP)',  # Added .iso files to the Playstation Portable (PSP) folder
    #'cso': 'Playstation Portable (PSP)',  # Added .cso files to the Playstation Portable (PSP) folder
    #'iso': 'Nintendo Wii',  # Added .iso files to the Nintendo Wii folder
    #'wbfs': 'Nintendo Wii',  # Added .wbfs files to the Nintendo Wii folder
    #'iso': 'Xbox',  # Added .iso files to the Xbox folder
    #'iso': 'Xbox 360',  # Added .iso files to the Xbox 360 folder
    #'xex': 'Xbox 360',  # Added .xex files to the Xbox 360 folder
    #'iso': 'Playstation 3',  # Added .iso files to the Playstation 3 folder
    #'pkg': 'Playstation 3',  # Added .pkg files to the Playstation 3 folder
    
}

def extract_and_move(file_path, extract_folder, source_folder, total_files, progress_bar, progress_label):
    # Create a temporary extraction folder
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)
    
    # Extract the archive
    if file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
    elif file_path.endswith('.7z'):
        with py7zr.SevenZipFile(file_path, 'r') as seven_zip_ref:
            seven_zip_ref.extractall(extract_folder)

    # Move files to their respective folders
    moved_files = []
    idx = 0
    for filename in os.listdir(extract_folder):
        idx += 1
        file_extension = filename.split('.')[-1].lower()
        if file_extension in rom_folders:
            dest_folder = os.path.join(source_folder, rom_folders[file_extension])
            # Ensure destination folder exists
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            shutil.move(os.path.join(extract_folder, filename), os.path.join(dest_folder, filename))
            moved_files.append((rom_folders[file_extension], filename))
        else:
            print(f"File {filename} with extension {file_extension} is not being moved.")
        
        # Update progress label
        progress_label.config(text=f"Processing: {idx}/{total_files}")
        progress_bar["value"] = (idx / total_files) * 100
        root.update_idletasks()

    # Clean up the temporary extraction folder
    shutil.rmtree(extract_folder)

    return moved_files

def process_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        # Process the selected folder
        mapping = {}
        total_files = 0
        files_to_process = []
        
        # Count total files
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and (filename.endswith('.zip') or filename.endswith('.7z')):
                files_to_process.append(file_path)
                total_files += 1
        
        # Create a progress bar window
        progress_frame = tk.Toplevel(root)
        progress_frame.title("Processing Progress")
        progress_frame.geometry("300x100")
        progress_label = tk.Label(progress_frame, text="Processing: 0/0")
        progress_label.pack(pady=5)
        progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=200, mode="determinate")
        progress_bar.pack(pady=5)
        
        # Process each file in the source folder
        for idx, file_path in enumerate(files_to_process, 1):
            moved_files = extract_and_move(file_path, os.path.join(folder_path, 'temp_extraction'), folder_path, total_files, progress_bar, progress_label)
            for folder, file_name in moved_files:
                mapping.setdefault(folder, []).append(file_name)

            # Update progress label
            progress_label.config(text=f"Processing: {idx}/{total_files}")
            progress_bar["value"] = (idx / total_files) * 100
            root.update_idletasks()

        # Show completion message after all files have been processed
        messagebox.showinfo("Extraction and Sorting Complete", "All ROMs have been extracted and sorted into their respective folders.")
        show_mapping_window(mapping)

def show_mapping_window(mapping):
    # Create a new window to display the mapping
    mapping_window = tk.Toplevel(root)
    mapping_window.title("File Mapping")

    # Calculate number of columns needed
    num_columns = len(mapping)
    if num_columns == 0:
        return

    # Calculate maximum number of files in any folder
    max_files = max(len(files) for files in mapping.values())

    # Create a Frame for each column
    for idx, (folder, files) in enumerate(mapping.items()):
        frame = tk.Frame(mapping_window)
        frame.grid(row=0, column=idx, padx=5, pady=5, sticky="n")
        # Label for folder name
        folder_label = tk.Label(frame, text=folder, font=("Arial", 12, "bold"), anchor="n", justify="center")
        folder_label.pack(fill="x")
        # Labels for file names
        for file_name in files:
            short_name = file_name.split('(')[0].strip()  # Get only the game name
            file_label = tk.Label(frame, text=short_name, font=("Arial", 10), anchor="w", justify="left")
            file_label.pack(fill="x")

# Create a Tkinter window
root = tk.Tk()
root.title("Rom Processing and Sorting")
root.geometry("600x350")  # Set the size of the window

# Instructions label
instructions = """
Welcome to Rom Processing and Sorting!

This program helps you organize your ROM files by extracting them from ZIP or 7z archives and sorting them into folders based on their extensions.

To use the program:
1. Click the 'Select Folder' button below.
2. Choose a folder containing your ROM files.
3. The program will process the files, extract them, and sort them into folders.
4. After processing is complete, a window will display the mapping of files to their respective folders.

Note: Only files with .zip or .7z extensions will be processed.

Code Written By JackJohns0n
"""
instructions_label = tk.Label(root, text=instructions, justify="left", wraplength=580)
instructions_label.pack(pady=10)

# Button to select folder
select_button = tk.Button(root, text="Select Folder", command=process_folder)
select_button.pack(pady=10)

root.mainloop()
