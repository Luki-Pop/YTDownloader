import os
import sys
import shutil
import subprocess
import urllib.request
import zipfile
import winshell
from win32com.client import Dispatch


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

    print("[OK] Files copied")


def create_shortcut():
    desktop = winshell.desktop()
    path = os.path.join(desktop, "YTDownloader.lnk")
    target = sys.executable
    arguments = f'"{os.path.join(INSTALL_DIR, "gui.py")}"'
    icon = target

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = INSTALL_DIR
    shortcut.IconLocation = icon
    shortcut.save()

    print("[OK] Shortcut created on desktop")


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
