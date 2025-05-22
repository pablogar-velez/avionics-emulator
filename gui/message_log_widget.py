from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

class MessageLogWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        
        # Professional aerospace console style
        self.setStyleSheet("""
            QTextEdit {
                background-color: #0A0E14;
                color: #B8C2CC;
                border: 1px solid #1E293B;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                selection-background-color: #1E3A8A;
            }
        """)
        
        # Set monospaced font for better readability
        font = QFont()
        font.setFamily("Consolas")
        font.setPointSize(11)
        font.setStyleHint(QFont.TypeWriter)
        self.setFont(font)
        
        # Set custom color palette
        palette = self.palette()
        palette.setColor(QPalette.Base, QColor(10, 14, 20))
        palette.setColor(QPalette.Text, QColor(184, 194, 204))
        self.setPalette(palette)

    def append_message(self, message: str):
        # Format message with colors according to type
        if (
            "ERROR" in message
            or "FAULT" in message
            or "INJECT" in message.upper()
            or "Label:999" in message
        ):
            self.setTextColor(QColor(239, 68, 68))  # Red for errors
        elif "WARN" in message:
            self.setTextColor(QColor(234, 179, 8))   # Yellow for warnings
        elif "INFO" in message:
            self.setTextColor(QColor(34, 197, 94))  # Green for info
        else:
            self.setTextColor(QColor(96, 165, 250))  # Blue for regular messages
            
        self.append(f"⚡ {message}")
        self.setTextColor(QColor(184, 194, 204))  # Restore default color
        self.ensureCursorVisible()  # Auto-scroll to new message
