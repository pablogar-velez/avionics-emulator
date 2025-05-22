import sys
from PyQt5.QtWidgets import QApplication
from bus.bus_emulator import BusEmulator
from modules.gps import GPS
from modules.fms import FMS
from modules.efis import EFIS
from modules.autopilot import Autopilot
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    bus = BusEmulator()
    modules = {
        "GPS": GPS(bus),
        "FMS": FMS(bus),
        "EFIS": EFIS(bus),
        "Autopilot": Autopilot(bus)
    }

    for module in modules.values():
        module.start()

    main_window = MainWindow(bus, modules)
    main_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
