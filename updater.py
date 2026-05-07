import os
import requests
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPDATE_URL = "https://raw.githubusercontent.com/Luki-Pop/YTDownloader/master/"
FILES = ["main.py", "gui.py", "version.txt"]

def download_file(name):
    url = UPDATE_URL + name
    r = requests.get(url, timeout=5)
    if r.status_code == 200:
        with open(os.path.join(BASE_DIR, name + ".new"), "wb") as f:
            f.write(r.content)

def apply_pending_update():
    for name in FILES:
        new_file = os.path.join(BASE_DIR, name + ".new")
        if os.path.exists(new_file):
            shutil.move(new_file, os.path.join(BASE_DIR, name))

def main():
    try:
        for name in FILES:
            download_file(name)
    except:
        pass

if __name__ == "__main__":
    main()
