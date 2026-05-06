import subprocess
import os
import sys
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_python(script):
    python = shutil.which("python") or shutil.which("python3")
    if not python:
        raise RuntimeError("Python not found in PATH")
    subprocess.call([python, os.path.join(BASE_DIR, script)])

def main():
    # 1. updater
    try:
        run_python("updater.py")
    except Exception as e:
        print("Updater error:", e)

    # 2. GUI
    try:
        run_python("gui.py")
    except Exception as e:
        print("GUI error:", e)

    # 3. apply update
    try:
        import updater
        updater.apply_pending_update()
    except Exception as e:
        print("Apply update error:", e)

if __name__ == "__main__":
    main()
