# Keylogger
This script is designed for record the keystroke 
How the script works on Windows:

    Adding to Startup: The script will add itself to the registry to run automatically when the user logs in.
    Hiding Console: The script hides the console window to run in the background silently (works on Windows only).
    Logging: It logs all keyboard and mouse events.
    Event Listeners: It listens for both keyboard and mouse events using the pynput library. You can customize the sleep time or behavior of the listeners if needed.

    To Run on Windows:

    Install Dependencies:
        Open a Command Prompt and install the required libraries using:

    pip install pynput pywin32

Run the Script:

    Save the script to a file (e.g., keylogger.py).
    Run the script from a Command Prompt window with Administrator privileges:

python keylogger.py

This will start the script on Windows, logging keyboard and mouse events, and adding itself to startup.
