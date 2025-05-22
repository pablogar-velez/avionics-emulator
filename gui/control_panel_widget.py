from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, 
    QFrame, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

class ControlPanelWidget(QWidget):
    def __init__(self, bus):
        super().__init__()
        self.bus = bus
        
        # General style of the panel
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 40, 50, 200);
                border-radius: 5px;
                border: 1px solid #4A6572;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        self.setLayout(layout)

        # Title of the panel
        title = QLabel("🛠️ FAULT INJECTION CONTROL PANEL")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: #4FC3F7;
                padding: 5px;
                border-bottom: 1px solid #4A6572;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Panel for selecting the type of fault
        fault_panel = QFrame()
        fault_panel.setStyleSheet("""
            QFrame {
                background-color: rgba(40, 50, 60, 150);
                border-radius: 4px;
                padding: 10px;
            }
        """)
        fault_layout = QVBoxLayout(fault_panel)
        fault_layout.setContentsMargins(8, 8, 8, 8)
        
        fault_label = QLabel("FAULT TYPE:")
        fault_label.setFont(QFont("Arial", 10, QFont.Bold))
        fault_label.setStyleSheet("color: #B0BEC5;")
        fault_layout.addWidget(fault_label)

        self.fault_type_combo = QComboBox()
        self.fault_type_combo.setFont(QFont("Arial", 10))
        self.fault_type_combo.addItems([
            "Select Fault Type",
            "Inject Invalid Data",
            "Inject Delay",
            "Inject Bit Flip",
            "Inject Drop Message"
        ])
        self.fault_type_combo.setStyleSheet("""
            QComboBox {
                background-color: #2C3E50;
                color: #ECEFF1;
                border: 1px solid #4A6572;
                padding: 6px;
                min-width: 200px;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                border-left: 1px solid #4A6572;
                width: 25px;
            }
            QComboBox QAbstractItemView {
                background: #2C3E50;
                color: #ECEFF1;
                selection-background-color: #4FC3F7;
                border: 1px solid #4A6572;
            }
        """)
        fault_layout.addWidget(self.fault_type_combo)
        layout.addWidget(fault_panel)

        # Panel for the inject button
        button_panel = QFrame()
        button_panel.setStyleSheet("background: transparent;")
        button_layout = QHBoxLayout(button_panel)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.inject_button = QPushButton("INJECT FAULT")
        self.inject_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.inject_button.setStyleSheet("""
            QPushButton {
                background-color: #D32F2F;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #F44336;
            }
            QPushButton:pressed {
                background-color: #B71C1C;
            }
            QPushButton:disabled {
                background-color: #455A64;
                color: #90A4AE;
            }
        """)
        self.inject_button.setCursor(Qt.PointingHandCursor)
        self.inject_button.clicked.connect(self.inject_fault)
        button_layout.addWidget(self.inject_button, 0, Qt.AlignCenter)
        layout.addWidget(button_panel)

        # Status indicator
        self.status_indicator = QLabel("STATUS: READY")
        self.status_indicator.setFont(QFont("Arial", 10, QFont.Bold))
        self.status_indicator.setStyleSheet("""
            QLabel {
                color: #81C784;
                padding: 5px;
                border-top: 1px solid #4A6572;
            }
        """)
        self.status_indicator.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_indicator)

    def inject_fault(self):
        fault_type = self.fault_type_combo.currentText()

        # Simple message mapping according to the selected fault_type
        fault_map = {
            "Inject Invalid Data": "Label:999 SDI:0 Data:ERROR SSM:0",
            "Inject Delay": "Label:999 SDI:0 Data:DELAY SSM:0",
            "Inject Bit Flip": "Label:999 SDI:0 Data:BITFLIP SSM:0",
            "Inject Drop Message": "Label:999 SDI:0 Data:DROP SSM:0"
        }

        if fault_type in fault_map:
            fault_msg = fault_map[fault_type]
            self.bus.transmit(fault_msg)
            self.status_indicator.setText(f"STATUS: INJECTED - {fault_type.upper()}")
            self.status_indicator.setStyleSheet("color: #FF8A65; font-weight: bold;")
        else:
            self.status_indicator.setText("STATUS: ERROR - NO FAULT SELECTED")
            self.status_indicator.setStyleSheet("color: #E57373; font-weight: bold;")

        # Reset status to READY after 3 seconds
        QTimer.singleShot(3000, lambda: [
            self.status_indicator.setText("STATUS: READY"),
            self.status_indicator.setStyleSheet("color: #81C784; font-weight: bold;")
        ])
