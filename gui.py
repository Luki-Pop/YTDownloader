import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal
from pytube import YouTube


class DownloadWorker(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, link):
        super().__init__()
        self.link = link

    def run(self):
        try:
            yt = YouTube(self.link)
            stream = yt.streams.get_highest_resolution()
            stream.download()
            self.finished.emit(True, "SUCCESS — You plunder the YouTube!")
        except Exception as e:
            self.finished.emit(False, f"ERROR: {str(e)}")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YT Downloader by Łukasz")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        self.label = QLabel("Wklej link do filmu:")
        layout.addWidget(self.label)

        self.input = QLineEdit()
        self.input.setPlaceholderText("https://youtube.com/...")
        layout.addWidget(self.input)

        self.button = QPushButton("Download")
        self.button.clicked.connect(self.start_download)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def start_download(self):
        link = self.input.text().strip()

        if not link:
            QMessageBox.warning(self, "Błąd", "Podaj link!")
            return

        self.button.setEnabled(False)
        self.worker = DownloadWorker(link)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, success, message):
        self.button.setEnabled(True)

        if success:
            QMessageBox.information(self, "OK", message)
        else:
            QMessageBox.critical(self, "Błąd", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
