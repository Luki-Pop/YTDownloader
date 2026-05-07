import subprocess
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

def run_python(script):
    python = shutil.which("python") or shutil.which("python3")
    if not python:
        raise RuntimeError("Python not found in PATH")

    log = os.path.join(BASE_DIR, "launcher.log")
    with open(log, "a", encoding="utf-8") as f:
        f.write(f"\n--- Running {script} ---\n")
        subprocess.call([python, os.path.join(BASE_DIR, script)], stdout=f, stderr=f)

def main():
    # 1. updater w tle
    try:
        python = shutil.which("python") or shutil.which("python3")
        subprocess.Popen([python, os.path.join(BASE_DIR, "updater.py")])
    except Exception as e:
        pass

    # 2. GUI
    try:
        run_python("gui.py")
    except Exception as e:
        pass

    # 3. apply update
    try:
        import updater
        updater.apply_pending_update()
    except Exception as e:
        pass

if __name__ == "__main__":
    main()
