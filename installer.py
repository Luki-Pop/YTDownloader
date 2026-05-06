import os
import sys
import shutil
import subprocess
import urllib.request
import zipfile


INSTALL_DIR = r"C:\Program Files\YTDownloader"
FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"


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


def download_ffmpeg():
    print("[INFO] Downloading FFmpeg...")
    zip_path = "ffmpeg.zip"
    urllib.request.urlretrieve(FFMPEG_URL, zip_path)

    print("[INFO] Extracting FFmpeg...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall("ffmpeg_temp")

    extracted_folder = os.listdir("ffmpeg_temp")[0]
    ffmpeg_bin = os.path.join("ffmpeg_temp", extracted_folder, "bin")

    print("[INFO] Installing FFmpeg to Program Files...")
    target = r"C:\Program Files\FFmpeg"
    os.makedirs(target, exist_ok=True)

    for file in os.listdir(ffmpeg_bin):
        shutil.copy(os.path.join(ffmpeg_bin, file), target)

    print("[INFO] Adding FFmpeg to PATH...")
    run(f'setx PATH "%PATH%;{target}"')

    shutil.rmtree("ffmpeg_temp")
    os.remove(zip_path)


def ensure_ffmpeg():
    if shutil.which("ffmpeg"):
        print("[OK] FFmpeg already installed")
    else:
        print("[INSTALL] FFmpeg not found — installing...")
        download_ffmpeg()


def install_app():
    print("[INFO] Installing YTDownloader...")

    os.makedirs(INSTALL_DIR, exist_ok=True)

    shutil.copy("main.py", INSTALL_DIR)
    shutil.copy("gui.py", INSTALL_DIR)

    # Tworzymy run.bat do uruchamiania aplikacji
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
