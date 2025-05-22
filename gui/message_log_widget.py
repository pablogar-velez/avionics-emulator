from PyQt5.QtWidgets import QTextEdit

class MessageLogWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("background-color: #111; color: #0f0; font-family: monospace;")

    def append_message(self, message: str):
        self.append(f"> {message}")
