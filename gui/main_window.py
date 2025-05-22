from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from gui.message_log_widget import MessageLogWidget
from gui.control_panel_widget import ControlPanelWidget
from messages.message_translator import translate_arinc429_message


class MainWindow(QWidget):
    def __init__(self, bus, modules):
        super().__init__()
        self.setWindowTitle("Avionics Systems Emulator - ARINC-429 Bus Monitor")
        self.setMinimumSize(1000, 700)
        
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(30, 30, 45))
        palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
        palette.setColor(QPalette.Base, QColor(20, 20, 30))
        palette.setColor(QPalette.AlternateBase, QColor(40, 40, 55))
        palette.setColor(QPalette.Button, QColor(50, 50, 70))
        palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
        palette.setColor(QPalette.Highlight, QColor(0, 150, 200))
        self.setPalette(palette)

        self.bus = bus
        self.modules = modules

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        # Header with aircraft-style design
        header = QLabel("✈ AVIONICS DATA BUS MONITOR - ARINC 429")
        header_font = QFont()
        header_font.setFamily("Arial")
        header_font.setPointSize(16)
        header_font.setWeight(QFont.Bold)
        header.setFont(header_font)
        header.setStyleSheet("color: #4FC3F7;")
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # Separator line (aircraft-style)
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #4A6572;")
        main_layout.addWidget(separator)

        # Filter panel with aircraft-style controls
        filter_panel = QFrame()
        filter_panel.setFrameShape(QFrame.StyledPanel)
        filter_panel.setStyleSheet("background-color: rgba(40, 40, 55, 150); border-radius: 5px;")
        filter_layout = QHBoxLayout(filter_panel)
        filter_layout.setContentsMargins(10, 10, 10, 10)
        
        filter_label = QLabel("MODULE FILTER:")
        filter_label.setFont(QFont("Arial", 10, QFont.Bold))
        filter_label.setStyleSheet("color: #B0BEC5;")
        
        self.filter_combo = QComboBox()
        self.filter_combo.setFont(QFont("Arial", 10))
        self.filter_combo.addItems(["ALL MODULES", "GPS", "FMS", "EFIS", "AUTOPILOT", "FAULT INJECTION"])
        self.filter_combo.currentTextChanged.connect(self.update_logs)
        self.filter_combo.setStyleSheet("""
            QComboBox {
                background-color: #2C3E50;
                color: #ECEFF1;
                border: 1px solid #4A6572;
                padding: 5px;
                min-width: 150px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background: #2C3E50;
                color: #ECEFF1;
                selection-background-color: #4FC3F7;
            }
        """)
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addStretch()
        main_layout.addWidget(filter_panel)

        # Message consoles container with aircraft panel style
        consoles_panel = QFrame()
        consoles_panel.setFrameShape(QFrame.StyledPanel)
        consoles_panel.setStyleSheet("background-color: rgba(20, 20, 30, 200); border: 1px solid #4A6572;")
        consoles_layout = QHBoxLayout(consoles_panel)
        consoles_layout.setContentsMargins(5, 5, 5, 5)
        consoles_layout.setSpacing(10)
        main_layout.addWidget(consoles_panel, 1)

        # Translated message log (left panel)
        translated_panel = QFrame()
        translated_panel.setFrameShape(QFrame.StyledPanel)
        translated_panel.setStyleSheet("background-color: #111827; border: 1px solid #334155;")
        translated_layout = QVBoxLayout(translated_panel)
        translated_layout.setContentsMargins(5, 5, 5, 5)
        
        translated_label = QLabel("TRANSLATED MESSAGES")
        translated_label.setFont(QFont("Arial", 10, QFont.Bold))
        translated_label.setStyleSheet("color: #4FC3F7; padding: 5px; border-bottom: 1px solid #334155;")
        translated_label.setAlignment(Qt.AlignCenter)
        
        self.translated_log = MessageLogWidget()
        translated_layout.addWidget(translated_label)
        translated_layout.addWidget(self.translated_log, 1)
        consoles_layout.addWidget(translated_panel, 1)

        # Raw message log (right panel)
        raw_panel = QFrame()
        raw_panel.setFrameShape(QFrame.StyledPanel)
        raw_panel.setStyleSheet("background-color: #111827; border: 1px solid #334155;")
        raw_layout = QVBoxLayout(raw_panel)
        raw_layout.setContentsMargins(5, 5, 5, 5)
        
        raw_label = QLabel("RAW ARINC-429 DATA")
        raw_label.setFont(QFont("Arial", 10, QFont.Bold))
        raw_label.setStyleSheet("color: #4FC3F7; padding: 5px; border-bottom: 1px solid #334155;")
        raw_label.setAlignment(Qt.AlignCenter)
        
        self.raw_log = MessageLogWidget()
        raw_layout.addWidget(raw_label)
        raw_layout.addWidget(self.raw_log, 1)
        consoles_layout.addWidget(raw_panel, 1)

        # Store messages as tuples: (translated_msg, raw_msg, module_name)
        self.all_messages = []

        # Control panel for fault injection (aircraft-style panel)
        self.control_panel = ControlPanelWidget(self.bus)
        main_layout.addWidget(self.control_panel)

        # Connect bus signal
        self.bus.message_transmitted.connect(self.receive_message)

    def receive_message(self, msg_str):
        from messages.message_format import ARINC429Message

        try:
            parts = msg_str.split()
            label = int(parts[0].split(":")[1])
            sdi = int(parts[1].split(":")[1])
            data_str = parts[2].split(":")[1]
            data = int(data_str) if data_str.isdigit() else data_str
            ssm = int(parts[3].split(":")[1])
            msg = ARINC429Message(label=label, sdi=sdi, data=data, ssm=ssm)
        except Exception:
            if "FAULT" in msg_str.upper() or "INJECT" in msg_str.upper():
                module_name = "FaultInjection"
            else:
                module_name = "Unknown"
            self.all_messages.append(("[RAW UNPARSED]", msg_str, module_name))
            self.update_logs()
            return

        translated = translate_arinc429_message(msg)
        module_name = self.label_to_module(label)

        if "fault" in translated.lower() or "inject" in translated.lower():
            module_name = "FaultInjection"

        self.all_messages.append((translated, msg_str, module_name))
        self.update_logs()

    def update_logs(self):
        selected_filter = self.filter_combo.currentText()
        self.translated_log.clear()
        self.raw_log.clear()

        for translated_msg, raw_msg, module_name in self.all_messages:
            show = False
            if selected_filter == "ALL MODULES":
                show = True
            elif selected_filter == "FAULT INJECTION":
                show = (module_name == "FaultInjection")
            else:
                show = (module_name == selected_filter)

            if show:
                self.translated_log.append_message(translated_msg)
                self.raw_log.append_message(raw_msg)

    @staticmethod
    def label_to_module(label):
        mapping = {
            101: "GPS",
            202: "FMS",
            303: "EFIS",
            404: "AUTOPILOT"
        }
        return mapping.get(label, "Unknown")