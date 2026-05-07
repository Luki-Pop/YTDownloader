import subprocess
import os
import sys
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

LOCKFILE = os.path.join(BASE_DIR, "app.lock")

def check_single_instance():
    if os.path.exists(LOCKFILE):
        sys.exit(0)
    with open(LOCKFILE, "w") as f:
        f.write("1")

def remove_lock():
    if os.path.exists(LOCKFILE):
        os.remove(LOCKFILE)

def run_python(script):
    python = shutil.which("python") or shutil.which("python3")
    if not python:
        raise RuntimeError("Python not found in PATH")

    log = os.path.join(BASE_DIR, "launcher.log")
    with open(log, "a", encoding="utf-8") as f:
        f.write(f"\n--- Running {script} ---\n")
        f.flush()
        result = subprocess.call(
            [python, os.path.join(BASE_DIR, script)],
            stdout=f,
            stderr=f
        )
        f.write(f"Return code: {result}\n")
        return result

def main():
    check_single_instance()

    try:
        python = shutil.which("python") or shutil.which("python3")
        subprocess.Popen([python, os.path.join(BASE_DIR, "updater.py")])
    except Exception:
        pass

    try:
        result = run_python("gui.py")
    except Exception:
        result = -1

    try:
        import updater
        updater.apply_pending_update()
    except Exception:
        pass

    if result == 0:
        remove_lock()

if __name__ == "__main__":
    main()
