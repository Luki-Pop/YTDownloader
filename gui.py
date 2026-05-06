import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QComboBox
)
from PyQt6.QtCore import QThread, pyqtSignal
from pytube import YouTube


# -------------------------
#   TŁUMACZENIA
# -------------------------
TRANSLATIONS = {
    "pl": {
        "title": "YT Downloader by Łukasz",
        "paste_link": "Wklej link do filmu:",
        "placeholder": "https://youtube.com/...",
        "download": "Pobierz",
        "success": "SUKCES — You plunder the YouTube!",
        "error": "BŁĄD: ",
        "empty": "Podaj link!",
        "lang_label": "Język:"
    },
    "en": {
        "title": "YT Downloader by Łukasz",
        "paste_link": "Paste video link:",
        "placeholder": "https://youtube.com/...",
        "download": "Download",
        "success": "SUCCESS — You plunder the YouTube!",
        "error": "ERROR: ",
        "empty": "Please enter a link!",
        "lang_label": "Language:"
    }
}


# -------------------------
#   WORKER (pobieranie)
# -------------------------
class DownloadWorker(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, link, lang):
        super().__init__()
        self.link = link
        self.lang = lang

    def run(self):
        try:
            yt = YouTube(self.link)
            stream = yt.streams.get_highest_resolution()
            stream.download()
            self.finished.emit(True, TRANSLATIONS[self.lang]["success"])
        except Exception as e:
            self.finished.emit(False, TRANSLATIONS[self.lang]["error"] + str(e))


# -------------------------
#   GŁÓWNE OKNO
# -------------------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.lang = "pl"  # domyślny język

        self.setWindowTitle(TRANSLATIONS[self.lang]["title"])
        self.setMinimumWidth(420)

        layout = QVBoxLayout()

        # wybór języka
        self.lang_label = QLabel(TRANSLATIONS[self.lang]["lang_label"])
        layout.addWidget(self.lang_label)

        self.lang_select = QComboBox()
        self.lang_select.addItem("Polski", "pl")
        self.lang_select.addItem("English", "en")
        self.lang_select.currentIndexChanged.connect(self.change_language)
        layout.addWidget(self.lang_select)

        # etykieta
        self.label = QLabel(TRANSLATIONS[self.lang]["paste_link"])
        layout.addWidget(self.label)

        # pole tekstowe
        self.input = QLineEdit()
        self.input.setPlaceholderText(TRANSLATIONS[self.lang]["placeholder"])
        layout.addWidget(self.input)

        # przycisk
        self.button = QPushButton(TRANSLATIONS[self.lang]["download"])
        self.button.clicked.connect(self.start_download)
        layout.addWidget(self.button)

        self.setLayout(layout)

    # -------------------------
    #   ZMIANA JĘZYKA
    # -------------------------
    def change_language(self):
        self.lang = self.lang_select.currentData()

        self.setWindowTitle(TRANSLATIONS[self.lang]["title"])
        self.lang_label.setText(TRANSLATIONS[self.lang]["lang_label"])
        self.label.setText(TRANSLATIONS[self.lang]["paste_link"])
        self.input.setPlaceholderText(TRANSLATIONS[self.lang]["placeholder"])
        self.button.setText(TRANSLATIONS[self.lang]["download"])

    # -------------------------
    #   START POBIERANIA
    # -------------------------
    def start_download(self):
        link = self.input.text().strip()

        if not link:
            QMessageBox.warning(self, "Error", TRANSLATIONS[self.lang]["empty"])
            return

        self.button.setEnabled(False)
        self.worker = DownloadWorker(link, self.lang)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    # -------------------------
    #   KONIEC POBIERANIA
    # -------------------------
    def on_finished(self, success, message):
        self.button.setEnabled(True)

        if success:
            QMessageBox.information(self, "OK", message)
        else:
            QMessageBox.critical(self, "Error", message)


# -------------------------
#   START APLIKACJI
# -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
