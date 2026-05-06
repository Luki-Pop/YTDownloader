import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QComboBox
)
from PyQt6.QtCore import QThread, pyqtSignal

from main import download_video  # <-- import logiki pobierania


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
        "quality": "Jakość:"
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
        "quality": "Quality:"
    }
}


# -------------------------
#   WORKER (wątek)
# -------------------------
class DownloadWorker(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, link, quality, lang):
        super().__init__()
        self.link = link
        self.quality = quality
        self.lang = lang

    def run(self):
        success, msg = download_video(self.link, self.quality)

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

        # przycisk
        self.button = QPushButton(TRANSLATIONS[self.lang]["download"])
        self.button.clicked.connect(self.start_download)
        layout.addWidget(self.button)

        self.setLayout(layout)

    # zmiana języka
    def change_language(self):
        self.lang = self.lang_select.currentData()

        self.setWindowTitle(TRANSLATIONS[self.lang]["title"])
        self.lang_label.setText(TRANSLATIONS[self.lang]["lang_label"])
        self.label.setText(TRANSLATIONS[self.lang]["paste_link"])
        self.input.setPlaceholderText(TRANSLATIONS[self.lang]["placeholder"])
        self.button.setText(TRANSLATIONS[self.lang]["download"])
        self.quality_label.setText(TRANSLATIONS[self.lang]["quality"])

    # start pobierania
    def start_download(self):
        link = self.input.text().strip()
        quality = self.quality_select.currentData()

        if not link:
            QMessageBox.warning(self, "Error", TRANSLATIONS[self.lang]["empty"])
            return

        self.button.setEnabled(False)
        self.worker = DownloadWorker(link, quality, self.lang)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    # koniec pobierania
    def on_finished(self, success, message):
        self.button.setEnabled(True)

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
