from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
)
from gui.message_log_widget import MessageLogWidget
from gui.control_panel_widget import ControlPanelWidget
from messages.message_translator import translate_arinc429_message

class MainWindow(QWidget):
    def __init__(self, bus, modules):
        super().__init__()
        self.setWindowTitle("Avionics Systems Emulator")
        self.setMinimumSize(800, 500)

        self.bus = bus
        self.modules = modules

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Header
        header = QLabel("🛰️ Avionics Data Bus Monitor")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(header)

        # Filter bar
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter by Module:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "GPS", "FMS", "EFIS", "Autopilot"])
        self.filter_combo.currentTextChanged.connect(self.update_filter)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        layout.addLayout(filter_layout)

        # Message log
        self.message_log = MessageLogWidget()
        layout.addWidget(self.message_log)

        # Control panel for fault injection
        self.control_panel = ControlPanelWidget(self.bus)
        layout.addWidget(self.control_panel)

        # Store all messages for filtering
        self.all_messages = []  # List of (translated_message, module_name)

        # Connect signal from the bus to receive messages
        self.bus.message_transmitted.connect(self.receive_message)

    def receive_message(self, msg_str):
        from messages.message_format import ARINC429Message

        try:
            # Attempt to parse ARINC429 format
            parts = msg_str.split()
            label = int(parts[0].split(":")[1])
            sdi = int(parts[1].split(":")[1])
            data = parts[2].split(":")[1]
            data = int(data) if data.isdigit() else data
            ssm = int(parts[3].split(":")[1])
            msg = ARINC429Message(label=label, sdi=sdi, data=data, ssm=ssm)
        except Exception:
            self.message_log.append_message(f"[RAW] {msg_str}")
            return

        translated = translate_arinc429_message(msg)
        module_name = self.label_to_module(label)

        self.all_messages.append((translated, module_name))

        selected_filter = self.filter_combo.currentText()
        if selected_filter == "All" or selected_filter == module_name:
            self.message_log.append_message(translated)

    def update_filter(self, selected_filter):
        self.message_log.clear()
        for msg, module_name in self.all_messages:
            if selected_filter == "All" or selected_filter == module_name:
                self.message_log.append_message(msg)

    @staticmethod
    def label_to_module(label):
        mapping = {
            101: "GPS",
            202: "FMS",
            303: "EFIS",
            404: "Autopilot",
            505: "EFIS",
            606: "EFIS",
            707: "EFIS",
            808: "Autopilot",
            909: "FMS",
            999: "Unknown"
        }
        return mapping.get(label, "Unknown")
