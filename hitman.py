# improved_activity_logger.py

import time
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
LOG_FILE = Path("history_log.txt")
CHECK_INTERVAL = 3  # seconds
PRINT_TO_CONSOLE = True


# =========================
# HELPER FUNCTIONS
# =========================
def get_active_window_title():
    """
    Safely gets the current active window title.
    """
    try:
        window = gw.getActiveWindow()

        if window and window.title:
            return window.title.strip()

        return "No Active Window"

    except Exception as e:
        return f"Window Detection Error: {e}"


def write_log(message):
    """
    Writes a message to the log file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"

    try:
        with LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(log_entry)

        if PRINT_TO_CONSOLE:
            print(log_entry, end="")

    except Exception as e:
        print(f"Failed to write log: {e}")


# =========================
# MAIN LOGGER
# =========================
def main():
    print("\n" + "=" * 50)
    print("        ██████╗ ██████╗  █████╗  ██████╗ ")
    print("        ██╔══██╗██╔══██╗██╔══██╗██╔═══██╗")
    print("        ██████╔╝██████╔╝███████║██║   ██║")
    print("        ██╔═══╝ ██╔══██╗██╔══██║██║   ██║")
    print("        ██║     ██║  ██║██║  ██║╚██████╔╝")
    print("        ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ")
    print("\n            PROJECT: BLACKOUT")
    print("         SYSTEM INITIALIZING...")
    print("=" * 50 + "\n")
    print("DEVELOPER NAME: EPSON CHIMUKWAYA, SHAUN .D. KALUBA ,DAVID MWALE AND MISHECK SG NG'AMBI")
    print("helper: EMMANUEL MWAMBA THEE GREAT")
    print('LOCATION: LUSAKA ZAMBIA')
    
    print("===================================")
    print(" Activity Logger Started")
    print(f" Log File: {LOG_FILE.resolve()}")
    print(" Press Ctrl+C to stop")
    print("===================================\n")

    last_window = None

    try:
        while True:
            current_window = get_active_window_title()

            # Log only when window changes
            if current_window != last_window:
                write_log(current_window)
                last_window = current_window

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\nLogger stopped safely.")

    except Exception as e:
        print(f"\nUnexpected error: {e}")


# =========================
# PROGRAM ENTRY
# =========================
if __name__ == "__main__":
    main()
