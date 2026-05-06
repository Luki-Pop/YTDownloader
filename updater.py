import requests
import os
import sys
import shutil

GITHUB_RAW = "https://raw.githubusercontent.com/Luki-Pop/YTDownloader/master/"
LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))

def download_file(filename):
    url = GITHUB_RAW + filename
    print(f"[UPDATE] Downloading {url}")
    r = requests.get(url)
    if r.status_code == 200:
        with open(os.path.join(LOCAL_DIR, filename), "wb") as f:
            f.write(r.content)
        return True
    return False

def get_remote_version():
    try:
        r = requests.get(GITHUB_RAW + "version.txt")
        return r.text.strip()
    except:
        return None

def get_local_version():
    try:
        with open(os.path.join(LOCAL_DIR, "version.txt"), "r") as f:
            return f.read().strip()
    except:
        return "0.0.0"

def update():
    local = get_local_version()
    remote = get_remote_version()

    print(f"[UPDATE] Local version: {local}")
    print(f"[UPDATE] Remote version: {remote}")

    if not remote or remote == local:
        print("[UPDATE] No update needed")
        return False

    print("[UPDATE] Updating files...")

    download_file("main.py")
    download_file("gui.py")
    download_file("version.txt")

    print("[UPDATE] Update complete")
    return True


if __name__ == "__main__":
    update()
