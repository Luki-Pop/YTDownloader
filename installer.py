import os
import sys
import shutil
import subprocess


INSTALL_DIR = r"C:\YTDownloader"   # bez Program Files → brak błędów


def run(cmd):
    print(f"[CMD] {cmd}")
    subprocess.call(cmd, shell=True)


def ensure_pip_package(pkg):
    try:
        __import__(pkg)
        print(f"[OK] {pkg} already installed")
    except ImportError:
        print(f"[INSTALL] Installing {pkg}...")
        run(f"pip install {pkg}")


def ensure_ffmpeg():
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"[OK] FFmpeg available at: {ffmpeg_path}")
    except Exception:
        print("[INSTALL] Installing FFmpeg via pip...")
        run("pip install imageio-ffmpeg")
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"[OK] FFmpeg installed at: {ffmpeg_path}")


def install_app():
    print("[INFO] Installing YTDownloader...")

    os.makedirs(INSTALL_DIR, exist_ok=True)

    shutil.copy("main.py", INSTALL_DIR)
    shutil.copy("gui.py", INSTALL_DIR)

    # Tworzymy run.bat
    with open(os.path.join(INSTALL_DIR, "run.bat"), "w") as f:
        f.write(f'@echo off\npython "{os.path.join(INSTALL_DIR, "gui.py")}"\n')

    print("[OK] Files copied")


def create_shortcut():
    print("[INFO] Creating desktop shortcut...")

    shortcut_ps = rf'''
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\YTDownloader.lnk")
$Shortcut.TargetPath = "{INSTALL_DIR}\run.bat"
$Shortcut.WorkingDirectory = "{INSTALL_DIR}"
$Shortcut.Save()
'''

    with open("create_shortcut.ps1", "w") as f:
        f.write(shortcut_ps)

    run("powershell -ExecutionPolicy Bypass -File create_shortcut.ps1")
    os.remove("create_shortcut.ps1")

    print("[OK] Shortcut created")


def main():
    print("=== YTDownloader Installer ===")

    print("\n[STEP] Checking Python packages...")
    ensure_pip_package("PyQt6")
    ensure_pip_package("yt_dlp")
    ensure_pip_package("imageio_ffmpeg")

    print("\n[STEP] Checking FFmpeg...")
    ensure_ffmpeg()

    print("\n[STEP] Installing application...")
    install_app()

    print("\n[STEP] Creating desktop shortcut...")
    create_shortcut()

    print("\n=== Installation complete! ===")
    print("You can now run YTDownloader from your desktop.")


if __name__ == "__main__":
    main()
