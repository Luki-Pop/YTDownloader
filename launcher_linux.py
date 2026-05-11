#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

LOCKFILE = os.path.join(BASE_DIR, ".app_lock")
LOGFILE = os.path.join(BASE_DIR, "launcher_linux.log")

logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format="%(asctime)s [LinuxLauncher] %(levelname)s: %(message)s"
)

def is_running():
    return os.path.exists(LOCKFILE)

def create_lock():
    with open(LOCKFILE, "w") as f:
        f.write(str(os.getpid()))

def remove_lock():
    if os.path.exists(LOCKFILE):
        os.remove(LOCKFILE)

def find_python():
    for exe in ["python3", "python"]:
        path = shutil.which(exe)
        if path:
            return path
    return None

def run_gui():
    python_exec = find_python()
    if not python_exec:
        logging.error("Python interpreter not found")
        print("Python3 is required but not installed.")
        return

    gui_path = os.path.join(BASE_DIR, "gui.py")

    logging.info(f"Launching GUI using {python_exec}")
    process = subprocess.Popen([python_exec, gui_path])

    return process

def main():
    logging.info("Linux launcher started")

    if is_running():
        logging.warning("Application already running")
        print("Application is already running.")
        return

    create_lock()

    try:
        process = run_gui()
        if process:
            process.wait()
    finally:
        remove_lock()
        logging.info("Linux launcher closed")

if __name__ == "__main__":
    main()
