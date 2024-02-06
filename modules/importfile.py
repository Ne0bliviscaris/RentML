# v1.01 - import file using system file pop-up dialog
import os
from tkinter import Tk, filedialog


# Manually browse for a file with a system file dialog window
def browse_files():
    """
    Opens a system file dialog and returns the relative path of the selected file.

    The function creates a hidden Tk root window, opens a file dialog for the user to select a file, and then converts the selected file's full path to a relative path.

    Returns:
        str: The relative path of the selected file.
    """
    root = Tk()
    root.withdraw()  # Hide the root window

    # Show the file dialog and store the selected file's full path
    file_path = filedialog.askopenfilename()
    # Convert the full path to a relative path
    relative_path = os.path.relpath(file_path)

    return relative_path
