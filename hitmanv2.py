import time
import csv
import subprocess
import platform
from datetime import datetime
from pathlib import Path

try:
    import pygetwindow as gw
except ImportError:
    print("Missing module.")
    print("Install with: pip install pygetwindow")
    raise SystemExit(1)


# =========================
# CONFIGURATION
# =========================
LOG_FILE = Path("activity_log.csv")
CHECK_INTERVAL = 1  # seconds
PRINT_TO_CONSOLE = True


# =========================
# HELPER FUNCTIONS
# =========================
def get_active_window_title():
    """
    Safely gets the current active window title.
    Handles Windows via pygetwindow and Linux via xdotool.
    """
    current_os = platform.system()
    
    # --- LINUX HANDLER ---
    if current_os == "Linux":
        try:
            # xdotool is a command-line tool for X11 on Linux
            # Command: Get the ID of the active window, then get its name
            cmd = ["xdotool", "getactivewindow", "getwindowname"]
            result = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
            title = result.decode("utf-8").strip()
            
            if title:
                return title
        except (FileNotFoundError, subprocess.SubprocessError):
            # If xdotool is missing, we fall back to pygetwindow (less reliable on Linux)
            # print("Warning: xdotool not found. Using fallback.")
            pass

    # --- WINDOWS & MAC (OR LINUX FALLBACK) ---
    try:
        window = gw.getActiveWindow()
        if window and window.title:
            return window.title.strip()
    except Exception:
        return "Unknown Window"

    return "No Active Window"


def write_log(start_time, end_time, window_title):
    """
    Writes activity data to the CSV log file.
    """
    duration_seconds = (end_time - start_time).total_seconds()
    
    # Format timestamps
    start_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = {
        "Start Time": start_str,
        "End Time": end_str,
        "Window Title": window_title,
        "Duration (sec)": round(duration_seconds, 2)
    }

    try:
        # Check if file exists to write header only once
        file_exists = LOG_FILE.exists()
        
        with LOG_FILE.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=log_entry.keys())
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(log_entry)

        if PRINT_TO_CONSOLE:
            print(f"[{end_str}] {window_title} ({round(duration_seconds, 2)}s)")

    except Exception as e:
        print(f"Failed to write log: {e}")


# =========================
# MAIN LOGGER
# =========================
def main():
    # ASCII ART & INTRO
    print("\n" + "=" * 50)
    print("        ██████╗ ██████╗  █████╗  ██████╗ ")
    print("        ██╔══██╗██╔══██╗██╔══██╗██╔═══██╗")
    print("        ██████╔╝██████╔╝███████║██║   ██║")
    print("        ██╔═══╝ ██╔══██╗██╔══██║██║   ██║")
    print("        ██║     ██║  ██║██║  ██║╚██████╔╝")
    print("        ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ")
    print("\n         PROJECT: BLACKOUT [V2.0]")
    print("      ENHANCED ACTIVITY TRACKING SYSTEM")
    print("=" * 50 + "\n")
    print("DEVELOPER NAME: EPSON CHIMUKWAYA, SHAUN .D. KALUBA ,DAVID MWALE AND MISHECK SG NG'AMBI")
    print("HELPER: EMMANUEL MWAMBA THEE GREAT")
    print('LOCATION: LUSAKA, ZAMBIA')
    
    print("===================================")
    print(" SYSTEM INITIALIZED...")
    print(f" OS Detected: {platform.system()}")
    print(f" Log File: {LOG_FILE.resolve()}")
    print(" Format: CSV (Compatible with Excel)")
    print(" Press Ctrl+C to stop safely")
    print("===================================\n")

    # Initialization
    session_start = datetime.now()
    last_window = get_active_window_title()
    window_start_time = session_start  # Track when the current window started
    
    # Log the session start
    print(f"Logging started at {session_start}")

    try:
        while True:
            time.sleep(CHECK_INTERVAL)
            current_window = get_active_window_title()
            now = datetime.now()

            # Log only when window changes
            if current_window != last_window:
                # Log the PREVIOUS window's duration
                write_log(window_start_time, now, last_window)
                
                # Update trackers for the NEW window
                last_window = current_window
                window_start_time = now

    except KeyboardInterrupt:
        # When stopping, log the final window's duration
        now = datetime.now()
        write_log(window_start_time, now, last_window)
        
        total_duration = (now - session_start).total_seconds() / 60
        print("\n" + "=" * 50)
        print(f"SESSION ENDED.")
        print(f"Total Session Time: {round(total_duration, 2)} minutes")
        print("Data saved successfully.")
        print("=" * 50)

    except Exception as e:
        print(f"\nUnexpected error: {e}")


# =========================
# PROGRAM ENTRY
# =========================
if __name__ == "__main__":
    main()
