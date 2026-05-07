import subprocess
import os
import sys
import shutil

# --- USTAWIENIE KATALOGU ROBOCZEGO ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# --- SINGLE INSTANCE LOCK ---
LOCKFILE = os.path.join(BASE_DIR, "app.lock")

def check_single_instance():
    if os.path.exists(LOCKFILE):
        # Aplikacja już działa → nie uruchamiamy ponownie
        sys.exit(0)
    with open(LOCKFILE, "w") as f:
        f.write("1")

def remove_lock():
    if os.path.exists(LOCKFILE):
        os.remove(LOCKFILE)

# --- URUCHAMIANIE Pythona Z LOGOWANIEM ---
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

# --- GŁÓWNA LOGIKA ---
def main():
    check_single_instance()

    # 1. Updater w tle (nie blokuje GUI)
    try:
        python = shutil.which("python") or shutil.which("python3")
        subprocess.Popen([python, os.path.join(BASE_DIR, "updater.py")])
    except Exception:
        pass

    # 2. Uruchomienie GUI
    try:
        result = run_python("gui.py")
    except Exception:
        result = -1

    # 3. Zastosowanie aktualizacji po zamknięciu GUI
    try:
        import updater
        updater.apply_pending_update()
    except Exception:
        pass

    # --- KLUCZOWE: USUWAMY LOCK TYLKO JEŚLI GUI ZAKOŃCZYŁO SIĘ POPRAWNIE ---
    if result == 0:
        remove_lock()
    else:
        # GUI crash → NIE usuwamy locka → brak pętli i brak wielu instancji
        pass

if __name__ == "__main__":
    main()
