import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_python(script):
    subprocess.call([sys.executable, os.path.join(BASE_DIR, script)])

def main():
    # 1. updater w tle
    try:
        run_python("updater.py")
    except Exception as e:
        print("Updater error:", e)

    # 2. uruchamiamy GUI
    run_python("gui.py")

    # 3. po zamknięciu GUI stosujemy aktualizacje
    try:
        import updater
        updater.apply_pending_update()
    except Exception as e:
        print("Apply update error:", e)

if __name__ == "__main__":
    main()
