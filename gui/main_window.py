from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from gui.message_log_widget import MessageLogWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Avionics Systems Emulator")
        self.setMinimumSize(600, 400)

        # Layout
        layout = QVBoxLayout()

        # Header
        header = QLabel("🛰️ Avionics Data Bus Monitor")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(header)

        # Message log widget
        self.message_log = MessageLogWidget()
        layout.addWidget(self.message_log)

        # Set main layout
        self.setLayout(layout)

        # Simulate test message (for now)
        self.message_log.append_message("Label=203, Source=GPS, Destination=FMS, Data=12345678")

    def receive_message(self, message_str):
        self.message_log.append_message(message_str)
