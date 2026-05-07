import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QComboBox,
    QProgressBar, QFileDialog
)
from PyQt6.QtCore import QThread, pyqtSignal

from main import download_video
import traceback

# -------------------------
# GUI LOG
# -------------------------

def debug_exceptions():
    def excepthook(type, value, tb):
        with open("gui_error.log", "w", encoding="utf-8") as f:
            traceback.print_exception(type, value, tb, file=f)
        sys.exit(1)
    sys.excepthook = excepthook


# -------------------------
#   TŁUMACZENIA
# -------------------------
TRANSLATIONS = {
    "pl": {
        "title": "YT Downloader by Łukasz",
        "paste_link": "Wklej link do filmu:",
        "placeholder": "https://youtube.com/...",
        "download": "Pobierz",
        "success": "SUKCES — pobieranie zakończone!",
        "error": "BŁĄD: ",
        "empty": "Podaj link!",
        "lang_label": "Język:",
        "quality": "Jakość:",
        "progress": "Postęp:",
        "choose_folder": "Wybierz folder",
        "folder_label": "Folder zapisu:"
    },
    "en": {
        "title": "YT Downloader by Łukasz",
        "paste_link": "Paste video link:",
        "placeholder": "https://youtube.com/...",
        "download": "Download",
        "success": "SUCCESS — download complete!",
        "error": "ERROR: ",
        "empty": "Please enter a link!",
        "lang_label": "Language:",
        "quality": "Quality:",
        "progress": "Progress:",
        "choose_folder": "Choose folder",
        "folder_label": "Save folder:"
    }
}


# -------------------------
#   WORKER (pobieranie)
# -------------------------
class DownloadWorker(QThread):
    finished = pyqtSignal(bool, str)
    progress_changed = pyqtSignal(float)

    def __init__(self, link, quality, save_path, lang):
        super().__init__()
        self.link = link
        self.quality = quality
        self.save_path = save_path
        self.lang = lang

    def run(self):
        def progress_callback(percent):
            self.progress_changed.emit(percent)

        success, msg = download_video(
            self.link,
            self.quality,
            self.save_path,
            progress_callback=progress_callback
        )

        if success:
            self.finished.emit(True, TRANSLATIONS[self.lang]["success"])
        else:
            self.finished.emit(False, TRANSLATIONS[self.lang]["error"] + msg)


# -------------------------
#   GŁÓWNE OKNO
# -------------------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.lang = "pl"
        self.save_path = os.path.expanduser("~/Downloads")

        self.setWindowTitle(TRANSLATIONS[self.lang]["title"])
        self.setMinimumWidth(420)

        layout = QVBoxLayout()

        # język
        self.lang_label = QLabel(TRANSLATIONS[self.lang]["lang_label"])
        layout.addWidget(self.lang_label)

        self.lang_select = QComboBox()
        self.lang_select.addItem("Polski", "pl")
        self.lang_select.addItem("English", "en")
        self.lang_select.currentIndexChanged.connect(self.change_language)
        layout.addWidget(self.lang_select)

        # link
        self.label = QLabel(TRANSLATIONS[self.lang]["paste_link"])
        layout.addWidget(self.label)

        self.input = QLineEdit()
        self.input.setPlaceholderText(TRANSLATIONS[self.lang]["placeholder"])
        layout.addWidget(self.input)

        # jakość
        self.quality_label = QLabel(TRANSLATIONS[self.lang]["quality"])
        layout.addWidget(self.quality_label)

        self.quality_select = QComboBox()
        self.quality_select.addItem("360p", "360p")
        self.quality_select.addItem("720p", "720p")
        self.quality_select.addItem("1080p", "1080p")
        self.quality_select.addItem("Audio only", "audio")
        layout.addWidget(self.quality_select)

        # folder zapisu
        self.folder_label = QLabel(TRANSLATIONS[self.lang]["folder_label"] + " " + self.save_path)
        layout.addWidget(self.folder_label)

        self.folder_button = QPushButton(TRANSLATIONS[self.lang]["choose_folder"])
        self.folder_button.clicked.connect(self.choose_folder)
        layout.addWidget(self.folder_button)

        # pasek postępu
        self.progress_label = QLabel(TRANSLATIONS[self.lang]["progress"])
        layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # przycisk pobierania
        self.button = QPushButton(TRANSLATIONS[self.lang]["download"])
        self.button.clicked.connect(self.start_download)
        layout.addWidget(self.button)

        self.setLayout(layout)


    # wybór folderu
    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.save_path = folder
            self.folder_label.setText(TRANSLATIONS[self.lang]["folder_label"] + " " + folder)

    # zmiana języka
    def change_language(self):
        self.lang = self.lang_select.currentData()

        self.setWindowTitle(TRANSLATIONS[self.lang]["title"])
        self.lang_label.setText(TRANSLATIONS[self.lang]["lang_label"])
        self.label.setText(TRANSLATIONS[self.lang]["paste_link"])
        self.input.setPlaceholderText(TRANSLATIONS[self.lang]["placeholder"])
        self.button.setText(TRANSLATIONS[self.lang]["download"])
        self.quality_label.setText(TRANSLATIONS[self.lang]["quality"])
        self.progress_label.setText(TRANSLATIONS[self.lang]["progress"])
        self.folder_button.setText(TRANSLATIONS[self.lang]["choose_folder"])
        self.folder_label.setText(TRANSLATIONS[self.lang]["folder_label"] + " " + self.save_path)

    # start pobierania
    def start_download(self):
        link = self.input.text().strip()
        quality = self.quality_select.currentData()

        if not link:
            QMessageBox.warning(self, "Error", TRANSLATIONS[self.lang]["empty"])
            return

        self.progress_bar.setValue(0)
        self.button.setEnabled(False)

        self.worker = DownloadWorker(link, quality, self.save_path, self.lang)
        self.worker.progress_changed.connect(self.update_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    # aktualizacja paska postępu
    def update_progress(self, percent):
        self.progress_bar.setValue(int(percent))

    # koniec pobierania
    def on_finished(self, success, message):
        self.button.setEnabled(True)
        self.progress_bar.setValue(100)

        if success:
            QMessageBox.information(self, "OK", message)
        else:
            QMessageBox.critical(self, "Error", message)


# start aplikacji
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
