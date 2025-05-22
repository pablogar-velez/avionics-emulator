import logging
from PyQt5.QtCore import QObject, pyqtSignal

logging.basicConfig(level=logging.INFO)

class BusEmulator(QObject):
    message_transmitted = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def transmit(self, msg: str):
        logging.info(f"Transmitting: {msg}")
        self.message_transmitted.emit(msg)
